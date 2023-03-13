from flask import Flask, redirect, url_for, request, render_template, session
from manipulationQuestion import *
from manipulationSequence import *
from manipulation_User import *
from md_mermaid import *
from markdownHTML import *
from manipulation_Etu import *
import hashlib
from flask_socketio import SocketIO 

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

@app.route("/") #Page principale du site
def index1():
    if 'Username' in session:
        if(session['type'] == "pro"):
            Username = session['Username']
            return render_template("acceuil_connecte.html", Username=Username)
        else:
            Username = session['Username']
            return render_template("acceuil_connecte_etu.html", Username=Username)
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
        return render_template("acceuil_connecte_etu.html", Username=Username)
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
                session['Username'] = nom_utilisateur
                IdUser = sous_liste[0]
                session['UserId'] = IdUser
                session['type'] = "etu"
                return render_template("acceuil_connecte_etu.html", Username=nom_utilisateur)
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


@app.route("/BDD") #Page d'accueil du compte avec la vue de toutes les questions créées et les étiquettes en haut, lorsqu'on clique sur une étiquette on ne voit plus que
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
    if 'Username' in session:
        Username = session['Username']
        nouveauMdp = request.form['newMdp']
        modificationEtu(Username, nouveauMdp)
        return render_template("changement_mdp_etu.html", Username=Username)
    else:
        return render_template("changement_mdp_etu")
            
                
                
                
@app.route("/afficheSequence/<id>") #page pour debuter une sequence
def afficheSequence(id):
    if 'Username' in session and session['type']=="pro":
        
        if(estDansCSV(id)):#Sequence
            print(lireSequence(session['UserId'], id))
            print(getQuestion(lireSequence(session['UserId'], id)[0],session["UserId"]))
            return render_template("sequence_prof.html", id_seq=id, dictionnaire=traductionUneQuestionToHTML(getQuestion(session["UserId"], lireSequence(session['UserId'], id)[0])), Username=session['Username'])
        else:
            return render_template("sequence_prof.html", id_seq=id, dictionnaire=traductionUneQuestionToHTML(getQuestion(session["UserId"], id)), Username=session['Username'])
    else:
        return render_template("sequence_eleve.html", id_seq=id)
        
        
@socketio.on('ouvrir_seq')#prof ouvre sequence
def ouvrir_q(id_seq):
    if 'UserId' or 'Username' in session and session['type'] == "pro":
            dico_question_ouverte_to_prof[id_seq]=session['UserId']
            li_prof_socket_id[id_seq]=request.sid
            dico_eleve_par_prof[session['UserId']]= []
            print(id_seq)
            print(estDansCSV(id_seq))
            if(not(estDansCSV(id_seq))): #le not() est temporaire car la fonction python est cassée
                pass
            else :
                seq = lireSequence(session["UserId"], id_seq)
                print(seq)
                if(len(seq)>0):
                    seq_id_to_seq_progress[id_seq] = seq[0]


        
    
@socketio.on('fermer_seq')#prof ferme sequence
def ouvrir_q(data):
    if 'UserId' or 'Username' in session and session['type'] == "pro":
        dico_question_ouverte_to_prof.pop(data)
        li_prof_socket_id.pop(data)
        dico_eleve_par_prof.pop(session['UserId'])
    


@socketio.on('questionSuivante')#prof avance sequence
def avancer_q(dic):
    id_seq = dic['id_seq']
    id_q = dic['id_q']
    print('demande de question suivante ', id_seq, id_q)
    li_eleve=dico_eleve_par_prof[session['UserId']]
    #recuperer contenu question suivante
    q_suiv = ""
    if (estDansCSV(id_seq) and id_q==""):
        ##question seule*
        print("demande question seule")
        q_suiv = getQuestion(session["UserID"], id_seq)
        q_suiv = traductionUneQuestionToHTML(q_suiv)
        print(q_suiv)
        socketio.emit("nouvelle_q", {'question':q_suiv}, room=li_eleve)
        socketio.emit("nouvelle_q", {'question':q_suiv}, room=request.sid)
    else:
        li_q = lireSequence(session['UserId'],id_seq)
        print("demande question suiv seq")
        i=0
        print(li_q)
        while(i< len(li_q) and li_q[i]!= id_q):
            i=i+1
            print(li_q[i], id_q)
        print(i, len(li_q))
        if (i>=len(li_q)):
            print("sequence terminer")
            socketio.emit("fin_seq", room=request.sid)
        else:
            q_suiv=li_q[i+1]
            seq_id_to_seq_progress[id_seq]=q_suiv
            
            #deux autre cas : derniere question, question de sequence
            print(q_suiv)
            print(getQuestion(session["UserId"], q_suiv))
            socketio.emit("nouvelle_q", {'question':traductionUneQuestionToHTML(getQuestion(session["UserId"], q_suiv))}, room=li_eleve)
            socketio.emit("nouvelle_q", {'question':traductionUneQuestionToHTML(getQuestion(session["UserId"], q_suiv))}, room=request.sid)
    
    
@socketio.on('stop_rep')#prof bloque rep
def bloquer_rep_q():
    li_eleve=dico_eleve_par_prof(session['UserId'])
    
    socketio.emit("bloquer_rep", room=li_eleve)
    

@socketio.on('eleve_reponse_q')#eleve reponds
def eleve_reponse_q(id_seq,reponse):
    #enregistrer rep
    #AJOUT ID_SEQ CODE SEQUENCE ELEVE
    prof = li_prof_socket_id(id_seq)
    socketio.emit("rep", {'reponse':reponse}, room=[prof])

@socketio.on('acceder_q')#eleve accede sequence
def acceder_q(id_seq):
    for eleme in dico_question_ouverte_to_prof.keys :
        if id_seq == eleme :
            currentSocketId = request.sid
            prof = dico_question_ouverte_to_prof.get(eleme)
            dico_eleve_par_prof[prof].append(currentSocketId)
            sess_id_prof = li_prof_socket_id[id_seq]
            #envoyer +1 prof
            q={}
            q_suiv=seq_id_to_seq_progress[id_seq]
            q["REP"]=traductionUneQuestionToHTML(getQuestion(session["UserId"], q_suiv))["REP"]
            q["Question"]=traductionUneQuestionToHTML(getQuestion(session["UserId"], q_suiv))["Question"]
            socketio.emit("nouvelle_q", {'question':traductionUneQuestionToHTML(getQuestion(session["UserId"], q_suiv))})

        
        
        #@app.route("/feuille")
#def feuille():                 
#    return render_template("feuille.html")

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug = True)# modifier le port si un autre groupe tourne déjà sur 5000 
    socketio.run(app)
