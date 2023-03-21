from flask import Flask, redirect, url_for, request, render_template, session
from manipulationQuestion import *
from manipulationSequence import *
from manipulation_User import *
from md_mermaid import *
from markdownHTML import *
from manipulation_Etu import *
from HistoQuestion import *
import hashlib
from flask_socketio import SocketIO 
from flask_socketio import join_room, leave_room
import time
import datetime
def new_date():
    """
    renvoie la date exact du jour,
    exemple: 2023/03/12/23/30/49.586607
    """
    mydate = str(datetime.datetime.now())
    print(mydate)
    mydate=list(mydate)
    for i in range (len(mydate)):
        if mydate[i] in ['-',':',' ']:
            mydate[i]='/'
    mydate = ''.join(mydate)
    return mydate

app = Flask(__name__)
app.secret_key = 'rfgcvgbhnj,k;k;,jhngfvcgfgbnh,jk;ljnhbgvfd'
app.config['UPLOAD_FOLDER'] = "upload"
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

li_ques_ouverte =[]# li session/question ouverte
dico_question_ouverte_to_prof = {}# id_q to userId prof
dico_eleve_par_prof ={}# user id prof to socket id eleve
li_prof_socket_id = {}#id q to session socket id du prof
seq_id_to_seq_progress = {}#seq_id_to_seq_progress
dico_seq_id_to_eleve_ayant_rep={}

@app.route("/") #Page principale du site
def index1():
    if 'Username' in session:
        if(session['type'] == "pro"):
            Username = session['Username']
            return render_template("acceuil_connecte.html", Username=Username)
        else:
            Username = session['Username']
            redirect
            return redirect(url_for('index2', Username=Username, pas_bon=False))
    else:
        return render_template("acceuil.html")

@app.route("/profil") #Page principale du site
def profil():
    if 'Username' and 'UserId' in session:
        if(session['type'] == "pro"):
            Username = session['Username']
            ID_User = session['UserId']
            return render_template("profil.html", Username=Username, liste=lireSequenceUser(ID_User))
        else:
            Username = session['Username']
            return render_template("profiletu.html", Username=Username)
    else:
        return render_template("acceuil.html")

@app.route("/acceuil_connecte_etu") #Page principale du site
def index2():
    if 'Username' in session:
        Username = session['Username']
        return render_template("acceuil_connecte_etu.html", Username=Username, pas_bon=False)
    else:
        return render_template("acceuil.html")

@app.route("/acceuil_connecte_etu", methods =['POST']) #Page principale du site
def accueiletu():
    if 'Username' in session:
        Username = session['Username']
        idSeq = request.form['idquest'] #id de sequence rentre
        if(idSeq not in li_ques_ouverte):
            return render_template("acceuil_connecte_etu.html", Username=Username, pas_bon=True)#On renvoie la personne sur la page d'accueil de l'etu mais avec une erreur 
        else:
            return redirect(url_for('afficheSequence',id = idSeq, Username=Username)) #On renvoie la personne sur la vue de la sequence demandee (si elle existe)
    else:
        return render_template("acceuil.html")
        

@app.route("/register") #Page de création d'un compte
def reg():
    return render_template("register.html", erreru=False)

@app.route("/register",methods = ['POST']) #Code d'enregistrement d'un utilisateur
def enregistrement():
    nom_utilisateur = request.form['idUser'] #On récupère son id
    email = request.form['email'] #Son mail
    mot_de_passe = request.form['password'] #Son mot de passe
    #mot_de_passe = hashlib.sha256(b)
    if ajouterUser(nom_utilisateur,hashlib.sha256(mot_de_passe.encode()).hexdigest(),email) == False:
        #print("le nom d'utilisateur ou le mail est déjà lié à un compte")
        return render_template("login.html", erreur=True)
    else:
        #print("compte créée")
        session['Username'] = nom_utilisateur
        session['type'] = "pro"
        csv = lireCSV()
        for User in csv:
            if User[1]==nom_utilisateur:
                IdUser = User[0]
                session['UserId'] = IdUser
        return render_template("acceuil_connecte.html", Username=nom_utilisateur)


@app.route("/login") #Page de connexion à un compte
def log():
    return render_template("login.html", erreur=False)

@app.route("/login",methods = ['POST']) #Code de connexion d'un utilisateur
def connexion():
    nom_utilisateur = request.form['idUser'] #On récupère son id
    mot_de_passe = request.form['password'] #Son mot de passe
    
    if request.form.get('typecompte', False) == 'on':
        listeetu = etuCSV()
        for sous_liste in listeetu:
            if sous_liste[2] == nom_utilisateur and sous_liste[3] == hashlib.sha256(mot_de_passe.encode()).hexdigest():
                #print("connexion")
                session['Username'] = sous_liste[0]
                IdUser = sous_liste[2]
                session['UserId'] = IdUser
                session['type'] = "etu"
                return redirect(url_for('index2', Username=sous_liste[0], pas_bon=False))
    else:
        listeUser = lireCSV()
        for sous_liste in listeUser:
            if sous_liste[1] == nom_utilisateur and sous_liste[3] == hashlib.sha256(mot_de_passe.encode()).hexdigest():
                #print("connexion")
                session['Username'] = nom_utilisateur
                IdUser = sous_liste[0]
                session['UserId'] = IdUser
                session['type'] = "pro"
                return render_template("acceuil_connecte.html", Username=nom_utilisateur)
    return render_template("login.html", erreur = True)
    #le mot de passe ou l'identifiant est incorrect


@app.route("/BDD") #Page d'acceuil du compte avec la vue de toutes les questions créées et les étiquettes en haut, lorsqu'on clique sur une étiquette on ne voit plus que
def BDD():          #les questions qui ont cette étiquette
    if 'UserId' and 'Username'in session and session['type'] == "pro":
        UserId = session['UserId']
        Username = session['Username']
        #print(UserId)
        dico = depuis_csv(UserId)
        dico=traductionQuestionToHTML(dico)
        #for question in dico:
            #for rep in question['REP']:
                #print(rep)
        return render_template("BDD.html", li_dictionnaire=dico, Username=Username)
    else:
        return render_template("non_connecte.html")

@app.route("/creationQuestion") #Page de création d'une question avec un nom, un énoncé, des réponses, une correction et des étiquettes
def creationQuestion():
    if 'Username' and 'UserId' in session and session['type'] == "pro":
        Username = session['Username']
        UserId = session['UserId']
        listeET = []
        listeQuestion = depuis_csv(UserId)
        for i in range(len(listeQuestion)):
            for j in range(len(listeQuestion[i]['ET'])):
                if listeQuestion[i]['ET'][j] not in listeET:
                    listeET.append(listeQuestion[i]['ET'][j])
        return render_template("creationQuestion.html", listeEtiquettes=listeET, Username=Username)
    else:
        return render_template("non_connecte.html")

@app.route("/creationQuestion",methods = ['POST']) #Code d'enregistrement d'une question une fois que toutes ses infos ont été rentrées pour une création
def ajoutQuestion():
    if 'UserId' and 'Username' in session and session['type'] == "pro":
        UserId = session['UserId']
        Username = session['Username']
        etiquettes = request.form.getlist('checkEti') #Ses étiquettes = str separé par ";"
        enonce = request.form['enonce'] #Son énoncé sous la forme markdown avec un titre mis en avant dans la bdd
        reponses = request.form['li_rep_possibles'] #Ses réponses
        reponses_pour_BREP = request.form['li_rep_possibles'].split(';') #Ses réponses sous forme de liste
        nb_reponses = request.form['nb_rep_possibles'] #Son nombre de bonnes réponses
        li_bonnes_reponses = [] #Initialisation de la liste des bonnes réponse
        #print(etiquettes + ' / ' + enonce + ' / ' + reponses + ' / ' + nb_reponses)
        if(nb_reponses!='1' and nb_reponses!='0'):
            for i in range(int(nb_reponses)): #Code de la liste des bonnes réponses
                if request.form.get(str(i), False) == 'on': #lorsque request.form[str(i)] est null, on a une erreur donc on utilise request.form.get(str(i), False) qui renvoie 'False' lorsque la requête est nulle (pas d'erreur) et 'on' sinon ('on' est renvoyé pour les réponses mises en bonnes réponses par l'utilisateur)
                    li_bonnes_reponses.append(reponses_pour_BREP[i]) #On ajoute à la liste des bonnes réponses l'indice des bonnes réponses
            li_rep = reponses.split(';')
            li_etiquettes = etiquettes
            li_etiquettes.append("QCM")
                    
        else:
            li_rep=[]
            li_bonnes_reponses.append(reponses)
            li_etiquettes = etiquettes
            li_etiquettes.append("QuestionOuverte")
        
        #print(etiquettes + ' / ' + enonce + ' / ' + reponses + ' / ' + str(nb_reponses) + ' / ')
         
        
        dictionnaire = {"Question": enonce, "ET": li_etiquettes, "REP": li_rep, "BREP": li_bonnes_reponses} #dictionnaire avec Question -> enoncé ; ET -> liste des étiquettes ; REP -> liste des réponses ; BREP -> liste des bonnes réponses
        
        idQ = str(dans_csv(UserId, dictionnaire)) #Ajout du dictionnaire d'une question dans le csv des questions
        return redirect(url_for('question',idQuestion = idQ, Username=Username)) #On renvoie la personne sur la vue de la question créée (si elle a bien été créée)
    else:
        return render_template("non_connecte.html")

@app.route("/visuIFrame",methods = ['POST']) #Code afin de visualiser une question en cours de creation
def visuIFrame():
        UserId = session['UserId']
        etiquettes = request.form.getlist('checkEti') #Ses étiquettes = str separé par ";"
        enonce = request.form['enonce'] #Son énoncé sous la forme markdown avec un titre mis en avant dans la bdd
        reponses = request.form['li_rep_possibles'] #Ses réponses
        reponses_pour_BREP = request.form['li_rep_possibles'].split(';') #Ses réponses sous forme de liste
        nb_reponses = request.form['nb_rep_possibles'] #Son nombre de bonnes réponses
        li_bonnes_reponses = [] #Initialisation de la liste des bonnes réponse
        #print(etiquettes + ' / ' + enonce + ' / ' + reponses + ' / ' + nb_reponses)
        for i in range(int(nb_reponses)): #Code de la liste des bonnes réponses
            if request.form.get(str(i), False) == 'on': #lorsque request.form[str(i)] est null, on a une erreur donc on utilise request.form.get(str(i), False) qui renvoie 'False' lorsque la requête est nulle (pas d'erreur) et 'on' sinon ('on' est renvoyé pour les réponses mises en bonnes réponses par l'utilisateur)
                li_bonnes_reponses.append(reponses_pour_BREP[i].replace("\r","")) #On ajoute à la liste des bonnes réponses l'indice des bonnes réponses
        #print(etiquettes + ' / ' + enonce + ' / ' + reponses + ' / ' + str(nb_reponses) + ' / ')
        li_etiquettes = etiquettes
        reponses = reponses.replace("\r","")
        li_rep = reponses.split(';')
        dict = {"idQ": 0,"Question": enonce.replace("\r",""), "ET": li_etiquettes, "REP": li_rep, "BREP": li_bonnes_reponses} #dictionnaire avec Question -> enoncé ; ET -> liste des étiquettes ; REP -> liste des réponses ; BREP -> liste des bonnes réponses
        #print(dict)
        return render_template("visuIFrame.html", dictionnaire=traductionUneQuestionToHTML(dict)) #on renvoie les donnée de la question sur l'IFrame de la page creation question

@app.route("/question/<idQuestion>") #Page de visualisation d'une question
def question(idQuestion):
    if 'Username' and 'UserId' in session and session['type'] == "pro":
        Username = session['Username']
        UserId = session['UserId']
        dico = getQuestion(UserId, idQuestion)
        #print(dico)
        dico = traductionUneQuestionToHTML(dico)

        return render_template("Question.html", dictionnaire=dico, Username=Username)
    else:
        return render_template("non_connecte.html")


@app.route("/import_eleve",methods = ['POST'])
def import_eleve():
    if 'Username' and 'UserId' in session and session['type'] == "pro":
        f = request.files['fichier']
        print(app.config['UPLOAD_FOLDER']+'/'+f.filename)
        f.save(app.config['UPLOAD_FOLDER']+'/'+f.filename)
        ajoutEtu(app.config['UPLOAD_FOLDER']+'/'+f.filename)
        return redirect(url_for('profil',Username=session['Username'], liste=lireSequenceUser(session['UserId'])))
    else:
        return render_template("non_connecte.html")


@app.route("/modificationQuestion/<idQuestion>") #Page de modification d'une question
def modifierQuestion(idQuestion):
    if 'Username' and 'UserId' in session and session['type'] == "pro":
        Username = session['Username']
        UserId = session['UserId']
        dico = getQuestion(UserId, idQuestion)
        listeET = []
        listeQuestion = depuis_csv(UserId)
        for i in range(len(listeQuestion)):
            for j in range(len(listeQuestion[i]['ET'])):
                if listeQuestion[i]['ET'][j] not in listeET:
                    listeET.append(listeQuestion[i]['ET'][j])
        return render_template("modificationQuestion.html", dictionnaire=dico, listeEtiquettes=listeET, Username=Username) #pour la modification il faut récupérer les infos existantes de la question et refaire la même chose qu'à la création
    else:
        return render_template("non_connecte.html")

@app.route("/modificationQuestion/<idQuestion>",methods = ['POST']) #Code d'enregistrement d'une question une fois que toutes ses infos ont été rentrées pour une modif
def modificationQuestion(idQuestion):
    if 'UserId' and 'Username' in session and session['type'] == "pro":
        UserId = session['UserId']
        Username = session['Username']
        etiquettes = request.form.getlist('checkEti') #Ses étiquettes = str separé par ";"
        enonce = request.form['enonce'] #Son énoncé sous la forme markdown avec un titre mis en avant dans la bdd
        reponses = request.form['li_rep_possibles'] #Ses réponses
        reponses_pour_BREP = request.form['li_rep_possibles'].split(';') #Ses réponses sous forme de liste
        nb_reponses = request.form['nb_rep_possibles'] #Son nombre de bonnes réponses
        li_bonnes_reponses = [] #Initialisation de la liste des bonnes réponse
        #print(etiquettes + ' / ' + enonce + ' / ' + reponses + ' / ' + nb_reponses)
        for i in range(int(nb_reponses)): #Code de la liste des bonnes réponses
            if request.form.get(str(i), False) == 'on': #lorsque request.form[str(i)] est null, on a une erreur donc on utilise request.form.get(str(i), False) qui renvoie 'False' lorsque la requête est nulle (pas d'erreur) et 'on' sinon ('on' est renvoyé pour les réponses mises en bonnes réponses par l'utilisateur)
                li_bonnes_reponses.append(reponses_pour_BREP[i]) #On ajoute à la liste des bonnes réponses l'indice des bonnes réponses
        #print(etiquettes + ' / ' + enonce + ' / ' + reponses + ' / ' + str(nb_reponses) + ' / ')
        li_etiquettes = etiquettes
        li_rep = reponses.split(';')
        dictionnaire = {"ID": idQuestion, "Question": enonce, "ET": li_etiquettes, "REP": li_rep, "BREP": li_bonnes_reponses} #dictionnaire avec Question -> enoncé ; ET -> liste des étiquettes ; REP -> liste des réponses ; BREP -> liste des bonnes réponses
        modif_csv(UserId, dictionnaire) #Ajout du dictionnaire d'une question dans le csv des questions
        return redirect(url_for('question',idQuestion = idQuestion, Username=Username)) #On renvoie la personne sur la vue de la question créée (si elle a bien été créée)
    else:
        return render_template("non_connecte.html")



@app.route("/creationFeuille") #Page dde création d'une feuille de questionse création d'une feuille de questions
def creationFeuille():
    if 'UserId' and 'Username' in session and session['type'] == "pro":
        UserId = session['UserId']
        Username = session['Username']
        #print(UserId)
        dico = depuis_csv(UserId)
        
        return render_template("creationFeuille.html",li_dictionnaire=traductionQuestionToHTML(dico), Username=Username)
    else:
        return render_template("non_connecte.html")

@app.route("/creationFeuille",methods = ['POST']) #La création d'une feuille 
def feuille():
    ListeIDQuestion=request.form.getlist('idQuestion')
    #print(ListeIDQuestion)
    if 'UserId' and 'Username'in session:
        UserId = session['UserId']
        Username = session['Username']
        maListeQuestion= []
        for ID in ListeIDQuestion:
            maListeQuestion.append(getQuestion(UserId,ID))
        
        #récupération de la liste d'id des exos de la feuille et renvoie à feuille.html
        return render_template("feuille.html", li_dictionnaire=traductionQuestionToHTML(maListeQuestion), Username=Username) 
    else:
        return render_template("non_connecte.html")


@app.route("/creationSequence") #Page dde création d'une feuille de questionse création d'une feuille de questions
def creationSequence():
    if 'UserId' and 'Username' in session and session['type'] == "pro":
        UserId = session['UserId']
        Username = session['Username']
        #print(UserId)
        dico = depuis_csv(UserId)
        
        return render_template("creationSequence.html",li_dictionnaire=traductionQuestionToHTML(dico), Username=Username)
    else:
        return render_template("non_connecte.html")

@app.route("/creationSequence",methods = ['POST']) #La création d'une feuille 
def Sequence():
    ListeIDQuestion=request.form.getlist('idQuestion')
    #print(ListeIDQuestion)
    if 'UserId' and 'Username'in session:
        UserId = session['UserId']
        Username = session['Username']
        ajouterSequence(UserId, ListeIDQuestion)
        return render_template("acceuil_connecte.html", Username=Username) 
    else:
        return render_template("non_connecte.html")


@app.route("/supprimer/<idQuestion>")
def supprimer(idQuestion):
    if 'UserId' in session and session['type'] == "pro":
        UserId = session['UserId']
        delQuestion(UserId,idQuestion)
        listedico=depuis_csv(UserId)
        return redirect(url_for('BDD'))
    else:
        return render_template("non_connecte.html")
@app.route("/supprimerHistoEt/<li>/<idQuestion>/<idetu>")
def supprimerHistoDirectEt(li,idQuestion,idetu):
    if 'UserId' in session and session['type'] == "pro":
        
        li = li.replace(" ","")
        li = li.replace("[","")
        li = li.replace("]","")
        li = li.replace("'","")
        li = li.replace("delimiteur","/")
        lif = li.split(",")
        
        lif[2]=idetu
        print("lif :",lif)
        li2=[lif[0],lif[1],idQuestion,lif[3]]
        if(lif[3]=="Sequence"):
            li2.append(lif[4])
        print("li2 :",li2)
        suppHisto(li2, idetu)
        #suppréssion dans le fichier étudiant 
        # ex:suppHisto(["date","FV","idQ","Sequence","idS"],"1258")
        supprimerUnHisto(lif, session["UserId"], idQuestion)
        #suppréssion dans le fichier étudiant 
        # ex:supprimerUnHisto(["07/04/2003","Faux","ve","Sequence","76"],1,2)
        ###########################################
        return redirect(url_for('Historique'))
    else:
        return render_template("non_connecte.html")
@app.route("/supprimerHisto/<li>/<idQuestion>")
def supprimerHistoDirect(li,idQuestion):
    if 'UserId' in session and session['type'] == "pro":
        
        li = li.replace(" ","")
        li = li.replace("[","")
        li = li.replace("]","")
        li = li.replace("'","")
        li = li.replace("delimiteur","/")
        lif = li.split(",")
        
        lif[2]
        print("lif :",lif)
        li2=[lif[0],lif[1],idQuestion,lif[3]]
        if(lif[3]=="Sequence"):
            li2.append(lif[4])
        print("li2 :",li2)
        suppHisto(li2, session["UserId"])
        supprimerUnHisto(lif, session["UserId"], idQuestion)
        ###########################################
        return redirect(url_for('Historique'))
    else:
        return render_template("non_connecte.html")

@app.route("/supprimerHistoComplet/<idQuestion>")
def supprimerHistoComplet(idQuestion):
    if 'UserId' in session and session['type'] == "pro":
        
        supprimerhistoQuestion(idQuestion)
        supprimerligne(session["UserId"], idQuestion)
        return redirect(url_for('Historique'))
    else:
        return render_template("non_connecte.html")



@app.route("/deco") #Page de création d'une feuille de questions
def deco():
    if 'UserId' or 'Username' in session and session['type'] == "pro":
        session.pop('UserId', None)
        session.pop('Username', None)
        session.pop('type', None)
        return redirect(url_for('index1'))
    else:
        return render_template("non_connecte.html")


@app.route("/sequence/<idQuestion>") #Page pour afficher q
def sequence(idQuestion):
    if 'UserId' or 'Username' in session and session['type'] == "pro":

        pass
    if 'UserId' or 'Username' in session and session['type'] == "etu":
        if li_ques_ouverte != []:
            trouve = False
            
@app.route("/changement_mdp_etu")
def modif_mdp_etu():
    if 'Username' in session:
        Username = session['Username']
        return render_template("changement_mdp_etu.html", Username=Username)
    else:
        return render_template("changement_mdp_etu")
    
@app.route("/changement_mdp_etu",methods = ['POST'])
def modif_mdp_etu_2():
    listeetu = etuCSV()
    UserId = session["UserId"]
    Username = session['Username']
    print(request.form['ancienMdp'], request.form['newMdp1'], request.form['newMdp2'])
    for sous_liste in listeetu: 
        if 'UserId' in session and sous_liste[2] == UserId:
            ancienMdp = request.form['ancienMdp']
            print(sous_liste[3], hashlib.sha256(ancienMdp.encode()).hexdigest())
            if sous_liste[3] != hashlib.sha256(ancienMdp.encode()).hexdigest():
                return render_template("changement_mdp_etu.html",erreur1=True) 
            elif request.form['newMdp1'] != request.form['newMdp2']:
                return render_template("changement_mdp_etu.html",erreur2=True)
            else:
                nouveauMdp = request.form['newMdp1']
                modificationEtu(UserId, nouveauMdp)
                return render_template("acceuil_connecte_etu.html",Username=Username)
            
                
                
                
@app.route("/afficheSequence/<id>") #page pour debuter une sequence
def afficheSequence(id):
    if 'Username' in session and session['type']=="pro":
        if(estDansCSV(id)):#Sequence
            #print(lireSequence(session['UserId'], id))
            #print(getQuestion(lireSequence(session['UserId'], id)[0],session["UserId"]))
            return render_template("sequence_prof.html", id_seq=id, Username=session['Username']) #, dictionnaire=traductionUneQuestionToHTML(getQuestion(session["UserId"], lireSequence(session['UserId'], id)[0]))
        else:
            return render_template("sequence_prof.html", id_seq=id, Username=session['Username']) #, dictionnaire=traductionUneQuestionToHTML(getQuestion(session["UserId"], id))
    elif('Username' in session and session['type']!="pro"):
            return render_template("sequence_eleve.html", id_seq=id, Username=session["Username"])
    else:
        render_template("acceuil.html")
        
        
@socketio.on('ouvrir_seq')#prof ouvre sequence
def ouvrir_q(id_seq):
    if 'UserId' or 'Username' in session and session['type'] == "pro":
            dico_question_ouverte_to_prof[id_seq]=session['UserId']
            li_prof_socket_id[id_seq]=request.sid
            dico_eleve_par_prof[session['UserId']]= []
            li_ques_ouverte.append(id_seq)
            print(id_seq)
            print(estDansCSV(id_seq))
            dico_seq_id_to_eleve_ayant_rep[id_seq]=[]
            if(not(estDansCSV(id_seq))): #question seule
                socketio.emit("nouvelle_q", {'question':traductionUneQuestionToHTML(getQuestion(session["UserId"], id_seq))})

            else :#sequence
                seq = lireSequence(session["UserId"], id_seq)
                print(seq)
                if(len(seq)>0):
                    seq_id_to_seq_progress[id_seq] = seq[0]
                    li_q = lireSequence(session['UserId'],id_seq)
                    q_suiv = li_q[0]
                    socketio.emit("nouvelle_q", {'question':traductionUneQuestionToHTML(getQuestion(session["UserId"], q_suiv))})



        
    
@socketio.on('fermer_seq')#prof ferme sequence
def fermer_seq(data):
    if 'UserId' in session and session['type'] == "pro":
        print("fermer seq serv")
        socketio.emit("fin_seq", to=session['UserId'])
        dico_question_ouverte_to_prof.pop(data)
        li_prof_socket_id.pop(data)
        dico_eleve_par_prof.pop(session['UserId'])
        li_ques_ouverte.pop(data)
        dico_seq_id_to_eleve_ayant_rep.pop(data)
        print("fin fermer seq serv")
    


@socketio.on('questionSuivante')#prof avance sequence
def avancer_q(dic):
    id_seq = dic['id_seq']
    id_q = dic['id_q']
    print('demande de question suivante ', id_seq, id_q)
    li_eleve=dico_eleve_par_prof[session['UserId']]
    #recuperer contenu question suivante
    q_suiv = ""
    if (not(estDansCSV(id_seq))):
        ##question seule*
        print("demande question seule")
        
        socketio.emit("fin_seq", room=session["UserId"])
        socketio.emit("fin_seq")
    else:#sequence
        li_q = lireSequence(session['UserId'],id_seq)
        print("demande question suiv seq")
        i=0
        print(li_q)
        print(id_q)
        while(i< len(li_q) and li_q[i]!= id_q):
            i=i+1
            print(li_q[i], id_q)
        print(i, len(li_q))
        if (i+1>=len(li_q)):
            print("sequence terminer")
            socketio.emit("fin_seq", room=session["UserId"])
            socketio.emit("fin_seq")
        else:
            dico_seq_id_to_eleve_ayant_rep[id_seq]=[]
            q_suiv=li_q[i+1]
            seq_id_to_seq_progress[id_seq]=q_suiv
            
            #deux autre cas : derniere question, question de sequence
            print(q_suiv)
            print(getQuestion(session["UserId"], q_suiv))
            
            q={}
            q["REP"]=traductionUneQuestionToHTML(getQuestion(session["UserId"], q_suiv))["REP"]
            q["Question"]=traductionUneQuestionToHTML(getQuestion(session["UserId"], q_suiv))["Question"]
            socketio.emit("nouvelle_q", {'question':q}, to=session["UserId"])
            socketio.emit("nouvelle_q", {'question':traductionUneQuestionToHTML(getQuestion(session["UserId"], q_suiv))}, to=request.sid)
    

@socketio.on('eleve_quitte')
def bloquer_rep_q(id_seq):
    for eleme in dico_question_ouverte_to_prof: #.keys()
        print("avant le if")
        if id_seq == eleme :
            print("après le if")
            
            prof = dico_question_ouverte_to_prof.get(eleme)
            sess_id_prof = li_prof_socket_id[id_seq]
            if(session['UserId'] in dico_eleve_par_prof[prof]):
                dico_eleve_par_prof[prof].remove(session['UserId'])
                print("envoie -1 prof")
                socketio.emit("eleve_a_quitter", to=li_prof_socket_id[id_seq])#envoyer -1 prof
                leave_room(prof)
            
            

@socketio.on('stop_rep')#prof bloque rep
def bloquer_rep_q():
    if 'UserId' in session and session['type'] == "pro":
        print("bloquer rep reçu")
        socketio.emit("bloquer_rep", to=session['UserId'])
    

@socketio.on('eleve_reponse_q')#eleve reponds
def eleve_reponse_q(id_seq,reponse):
    print(reponse)
    id_seq = id_seq["id_seq"]
    li_eleve_deja_rep = dico_seq_id_to_eleve_ayant_rep[id_seq]
    date_str=str(new_date())
    if(session["UserId"] not in li_eleve_deja_rep):
        #enregistrer rep
        if(estDansCSV(id_seq)):#c'est une sequence
            id_q = seq_id_to_seq_progress[id_seq]
            prof = dico_question_ouverte_to_prof[id_seq]
            enonce = getQuestion(prof, id_q)
            if(enonce["REP"]==[]):
                if(reponse==enonce["BREP"][0]):
                    ajouterHisto(prof, id_q, [date_str, "Vrai", session["UserId"], "Sequence", id_seq])
                    ajouterHistoEtu([date_str, "Vrai", id_q, "Sequence", id_seq], session["UserId"])
                else :
                    ajouterHisto(prof, id_q, [date_str, "Faux", session["UserId"], "Sequence", id_seq])
                    ajouterHistoEtu([date_str, "Faux", id_q, "Sequence", id_seq], session["UserId"])
            else:
                li_brep = enonce["BREP"]
                bonnerep = True
                for element in reponse:
                    if(enonce["REP"][element] in li_brep):
                        li_brep.remove(enonce["REP"][element])
                    else:
                        bonnerep = False
                    if(li_brep!=[]):
                        bonnerep = False
                if(bonnerep):
                    ajouterHisto(prof, id_q, [date_str, "Vrai", session["UserId"], "Sequence", id_seq])
                    ajouterHistoEtu([date_str, "Vrai", id_q, "Sequence", id_seq], session["UserId"])
                else:
                    ajouterHisto(prof, id_q, [date_str, "Faux", session["UserId"], "Sequence", id_seq])
                    ajouterHistoEtu([date_str, "Faux", id_q, "Sequence", id_seq], session["UserId"])
        else:#c'est une question seule
            id_q = id_seq
            prof = dico_question_ouverte_to_prof[id_seq]
            enonce = getQuestion(prof, id_q)
            if(enonce["REP"]==[]):
                if(reponse==enonce["BREP"][0]):
                    ajouterHisto(prof, id_q, [date_str, "Vrai", session["UserId"], "Direct"])
                    ajouterHistoEtu([date_str, "Vrai", id_q, "Direct"], session["UserId"])
                else :
                    ajouterHisto(prof, id_q, [date_str, "Faux", session["UserId"], "Direct"])
                    ajouterHistoEtu([date_str, "Faux", id_q, "Direct"], session["UserId"])
            else:
                li_brep = enonce["BREP"]
                bonnerep = True
                for element in reponse:
                    if(enonce["REP"][element] in li_brep):
                        li_brep.remove(enonce["REP"][element])
                    else:
                        bonnerep = False
                    if(li_brep!=[]):
                        bonnerep = False
                if(bonnerep):
                    ajouterHisto(prof, id_q, [date_str, "Vrai", session["UserId"], "Direct"])
                    ajouterHistoEtu([date_str, "Vrai", id_q, "Direct"], session["UserId"])
                else:
                    ajouterHisto(prof, id_q, [str(new_date()), "Faux", session["UserId"], "Direct"])
                    ajouterHistoEtu([str(new_date()), "Faux", id_q, "Direct"], session["UserId"])

    #AJOUT ID_SEQ CODE SEQUENCE ELEVE
        prof = li_prof_socket_id[id_seq]
        dico_seq_id_to_eleve_ayant_rep[id_seq].append(session["UserId"])
        socketio.emit("rep", {'reponse':reponse}, room=[prof])

@socketio.on('acceder_q')#eleve accede sequence
def acceder_q(id_seq):
    print(id_seq)
    print("session ouverte : ", dico_question_ouverte_to_prof)
    for eleme in dico_question_ouverte_to_prof: #.keys()
        print("avant le if")
        if id_seq["id_seq"] == eleme :
            print("après le if")
            
            prof = dico_question_ouverte_to_prof.get(eleme)
            sess_id_prof = li_prof_socket_id[id_seq["id_seq"]]
            if(session['UserId'] not in dico_eleve_par_prof[prof]):
                dico_eleve_par_prof[prof].append(session['UserId'])#envoyer +1 prof
                socketio.emit("nouveau_eleve", to=sess_id_prof)
                join_room(prof)
            
            
            q={}
            if(not(estDansCSV(id_seq["id_seq"]))):
                q_suiv=id_seq["id_seq"]
            else:
                q_suiv=seq_id_to_seq_progress[id_seq["id_seq"]]
            q["REP"]=traductionUneQuestionToHTML(getQuestion(prof, q_suiv))["REP"]
            q["Question"]=traductionUneQuestionToHTML(getQuestion(prof, q_suiv))["Question"]
            socketio.emit("nouvelle_q", {'question':q}, to=request.sid)
            print("requete envoyée")

def formatage_dict_etu(dict_q,dict_seq):
    dict_final={}
    for idQ in dict_q :
        if idQ in dict_final:
            dict_final[idQ].append(dict_q[idQ])
        else:
            dict_final[idQ]=dict_q[idQ]
    #print(dict_final)
    for idQ_seq in dict_seq :
        idQ=idQ_seq.split("seq")[0]
        seq=idQ_seq.split("seq")[1]
        if idQ in dict_final:
                
            dict_final[idQ]=dict_final[idQ]+dict_seq[idQ_seq]
                #.append(dict_seq[idQ_seq])
        else:
            #print("on reaffecte")
            dict_final[idQ]=dict_seq[idQ_seq]
    return dict_final

@app.route("/Historique") #Page de création d'une feuille de questions
def Historique():
    if 'UserId' or 'Username' in session and session['type'] == "pro":
        #print(dicoPourFaciliteLesStat(session['UserId']))
        #print(lireHisto(session['UserId']))
        #print(nbPositive(dicoPourFaciliteLesStat(session['UserId'])[0]))
        dict_q=dicoPourFaciliteLesStat(session['UserId'])[0]
        dict_seq=dicoPourFaciliteLesStat(session['UserId'])[1]
        dict_final={}
        dict_histogramme={}
        for idQ in dict_q :
            if idQ in dict_final:
                dict_final[idQ].append(dict_q[idQ])
            else:
                dict_final[idQ]=dict_q[idQ]
        #print(dict_final)
        for idQ_seq in dict_seq :
            idQ=idQ_seq.split("seq")[0]
            seq=idQ_seq.split("seq")[1]
            if idQ in dict_final:
                
                dict_final[idQ]=dict_final[idQ]+dict_seq[idQ_seq]
                #.append(dict_seq[idQ_seq])
            else:
                #print("on reaffecte")
                dict_final[idQ]=dict_seq[idQ_seq]
        #print(dict_final)
        for idQ in dict_final:
            dict_histogramme[idQ]=[]
            li_date=[]
            li_effectif=[]
            for rep in dict_final[idQ]:
                trouve=False
                date ="/".join(rep[0].split("/")[:3])
                for k in range(len(li_date)):
                    
                    if(date == li_date[k]):
                        li_effectif[k]=li_effectif[k]+1
                        trouve=True
                if trouve==False:
                    li_date.append(date)
                    li_effectif.append(1)
            
            dict_histogramme[idQ]=[li_date,li_effectif]
        li_etu = listedesEtudiant()
        dico_histo_etu={}
        for element in li_etu:
            dic_inter=dicoHistoetu(element)
                #print("dic inter",dic_inter)
            dico_histo_etu[element]=formatage_dict_etu(dic_inter[0],dic_inter[1])
            #print(dico_histo_etu)
        print(dict_final)
        return render_template("statsProf.html", Username=session['Username'], dico=dict_final, histo=dict_histogramme, dico_etu=dico_histo_etu)
    elif 'UserId' or 'Username' in session:
        return render_template("acceuil_connecte_etu.html")
    else:
        return render_template("acceuil.html")


#@app.route("/feuille")
#def feuille():                 
#    return render_template("feuille.html")

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug = True)# modifier le port si un autre groupe tourne déjà sur 5000 
    socketio.run(app)
