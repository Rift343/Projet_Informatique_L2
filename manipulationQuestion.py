import csv
import os
import markdownHTML
from random import randrange
littlePATH = "/csv"

def depuis_csv(ID_User):
    """
    Ouvre un fichier au format csv
    Renvoie une liste de dictionnaire avec clé disponible:
    ID=>id de la question (String)
    Question=> Enoncé de la question (String)
    ET => liste des étiquettes(liste de String)
    REP => liste de réponses possible (liste de String)
    BREP => liste des bonne réponse (liste de String)
    """    
    PATH = os.getcwd()
    #On récupere le PATH jusqu'au répertoire de travails
    PATH = PATH+littlePATH+"/question_"+str(ID_User)+".csv"#Au modifié pour correspondre dès que les csv seront changés de répertoires
    #On ajoute au PATH le chemin vers notre fichier
    #print(PATH)
    #print(os.path.isfile(PATH))
    if(not(os.path.isfile(PATH))):
        return []

    with open(PATH,'r') as FILE:#Ouverture du fichier
        lecture=csv.reader(FILE,delimiter=';')
        #Lecture du fichier csv avec pour délimiter ;
        ListeQuestion=[]
        for ligne in lecture:
            ListeQuestion.append(ligne)
            #on récupère les listes dans lecture afin de les écrire dans une liste de liste
        #Dans les lignes suivantes, l'on va récupérer les informations dans les différentes liste de listes
        #afin d'écrire c'est informations dans une liste de dictionnaire
        ListeDicoQuestion=list()
        for ligne in ListeQuestion:
            listeET=[]
            listeREP=[]
            ListeBREP=[]
            IDQuestion=ligne[0]
            compteur =1
            #print(ligne)
            while (ligne[compteur]!='FINET'):
                listeET.append(ligne[compteur])
                compteur=compteur+1
            compteur=compteur+1
            EnonceQuestion=ligne[compteur]
            compteur=compteur+1
            while (ligne[compteur]!='FINREP'):
                listeREP.append(ligne[compteur])
                compteur=compteur+1
            compteur=compteur+1
            while(compteur<len(ligne)):
                ListeBREP.append(ligne[compteur])
                compteur=compteur+1
            ListeDicoQuestion.append({'ID':IDQuestion,'Question':EnonceQuestion,'ET':listeET,'REP':listeREP,'BREP':ListeBREP})
    #print(ListeDicoQuestion)
    return ListeDicoQuestion
    
#print(depuis_csv("math"))

def traductionQuestionToHTML(listeDico):
    """
    Entré:listeDico-> une liste de dictionnaire sous format :
    ID=>id de la question (String)
    Question=> Enoncé de la question (String)
    ET => liste des étiquettes(liste de String)
    REP => liste de réponses possible (liste de String)
    BREP => liste des bonne réponse (liste de String)

    Sortie: La même liste mais les questions sont traduites en HTML
    """
    for i in listeDico:
        #print( i['Question'])
        i['Question']=markdownHTML.markdownToHtml(i['Question'])
        for x in range(len(i['REP'])):
            i['REP'][x] = markdownHTML.markdownToHtml(i['REP'][x])
        for y in range(len(i['BREP'])):
             i['BREP'][y] = markdownHTML.markdownToHtml(i['BREP'][y])
    #print(listeDico)    
    return listeDico

def traductionUneQuestionToHTML(dico):
    """
    Entré:listeDico-> un  dictionnaire sous format :
    ID=>id de la question (String)
    Question=> Enoncé de la question (String)
    ET => liste des étiquettes(liste de String)
    REP => liste de réponses possible (liste de String)
    BREP => liste des bonne réponse (liste de String)

    Sortie: la question traduite en HTML
    """

    dico['Question']=markdownHTML.markdownToHtml(dico['Question'])
    for r in range(len(dico['REP'])):
        dico['REP'][r]=markdownHTML.markdownToHtml(dico['REP'][r])
    for y in range(len(dico['BREP'])):
        dico['BREP'][y] = markdownHTML.markdownToHtml(dico['BREP'][y])
    return dico


#print(traductionQuestionToHTML(depuis_csv(3)))
#print(traductionQuestionToHTML(depuis_csv(1)))
#f= """```mermaid
#graph LR
#A --- B
#```
#"""
#print(f+"\n\n")
#print(markdownHTML.markdownToHtml(f))

def estDansCSV(ID_Question):
    """
    Entré: ID_User=> l'identifiant de l'utilisateur 
            ID_Question=>l'identifiant de la question que l'on cherche
    Sortie:True Si ID_Question et dans le fichier ID_Question ou False sinon
    Principe: On ouvre le ficher ID_Question.csv puis l'on recherche si il y a une occurence de ID_Question
    """
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"/ID_Question"+".csv"
    with open(PATH,'r') as FILE:
        lecture=csv.reader(FILE,delimiter=';')
        maliste=[]
        for ligne in lecture:
            maliste.append(ligne)
            for i in maliste:
                if (i[0]==ID_Question):
                    return False
            return True


def doublon(ID_User,Question,reponse):
    """
    Entrée: ID_User=>L'identifiant de l'utilisateur
            Question=> La question que l'on modifie
            reponse=> La réponse que l'on ajouter
    Sortie:Un boolean si la réponse et présente on doublon
    Cherche dans une question si la réponse n'est pas un doublon
    """
    maliste=depuis_csv(ID_User)
    for i in maliste:
        if (i['Question']==Question):
            if(i['REP']==reponse):
                return True
    return False



def dans_csv(ID_User,Dico_csv):
    """
    Entré: ID_User => id d'un utilisateur
           Dico_csv => une dictionnaire sous le format:
            Question=> Enoncé de la question (String)
            ET => liste des étiquettes(liste de String)
            REP => liste de réponses possible (liste de String)
            BREP => liste des bonne réponse (liste de String)
    Sortie: Rien

    Ecrit la question de Dico_csv dans le fichier contenant les questions de ID_User
    """
    li=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"]
    id ="AHYpV56e"
    ListeCSV=list()
    PATH= os.getcwd()
    PATH =  PATH+littlePATH+"/question_"+str(ID_User)+".csv"#Au modifié pour correspondre dès que les csv seront changés de répertoires
    #os.path.isfile() permet de savoir si le fichier correspondant au PATH existe
    #Si oui alors il faut attribuer à la 
    if(os.path.isfile(PATH)):
        #id=1
        while (estDansCSV(str(id))==False):
            id =""
            for i in range (8):
                id = id+li[randrange(len(li))]
        ListeCSV.append(id)
        #On regarde si on n'écrit pas un question en double. 
        #Si on écrit un question en double alors on return False
        if doublon(ID_User,Dico_csv['Question'],Dico_csv['REP']):
            return False
          
    else:
        #id=1
        while (estDansCSV(str(id))==False):
            id =""
            for i in range (8):
                id = id+li[randrange(len(li))]
        ListeCSV.append(id)

    for etiquette in Dico_csv['ET']:
        ListeCSV.append(etiquette)
    ListeCSV.append('FINET')
    ListeCSV.append(Dico_csv['Question'])
    for reponse in Dico_csv['REP']:
        ListeCSV.append(reponse)
    ListeCSV.append('FINREP')
    for BonneReponse in Dico_csv['BREP']:
        ListeCSV.append(BonneReponse)

    #print(ListeCSV)
    #Les lignes en dessous permettent une nouvelle ligne dans un csv
    #Si le csv n'existe pas alors il est automatiquement crée
    with open(PATH,'a',newline='') as FILE:
        Ecriture=csv.writer(FILE,delimiter=';')   
        Ecriture.writerow(ListeCSV)
        FILE.close()
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"/ID_Question"+".csv"
    with open(PATH,'a',newline='') as FILE:
        Ecriture=csv.writer(FILE,delimiter=';')   
        Ecriture.writerow([id,ID_User])
        FILE.close()  
    return id

#print(dans_csv(2,{'Question': 'Nb Ocet INT', 'ET': ['Info'], 'REP': ['2', '3', '4','5'], 'BREP': ['4']}) )    


def modif_csv(ID_User,Dico_csv):
    """
    Entrée: ID_User => id de l'utilisateur
            Dico_csv => dictionnaire au même format que la sortie de depuis_csv:
                ID=>id de la question (String)
                Question=> Enoncé de la question (String)
                ET => liste des étiquettes(liste de String)
                REP => liste de réponses possible (liste de String)
                BREP => liste des bonne réponse (liste de String)
    Sortie: True ou False si l'élément à modifier n'existe pas
    Exécution: On va regarde dans le fichier des questions de l'utilisateur 
    afin de vérifier si il possède bien la question que l'on veut modifier
    Ensuite on modifie tout les champs à l'éxeption de l'id et l'on doit réecrire toute
    les questions dans le fichiers
    """
    PATH= os.getcwd()
    PATH =  PATH+littlePATH+"/question_"+str(ID_User)+".csv"
    if (os.path.isfile(PATH)):
        lecture = depuis_csv(ID_User)
        for ligne in lecture:
            #On modifier seulement la question possèdant la même id.
            if (ligne['ID']==Dico_csv['ID']):
                ligne['Question']=Dico_csv['Question']
                ligne['ET']=Dico_csv['ET']
                ligne['REP']=Dico_csv['REP']
                ligne['BREP']=Dico_csv['BREP']
        
            
        ListeCSV=[];
        for dico in lecture:
            ListeCSV.append([])
            ListeCSV[-1].append(dico['ID'])
            for i in dico['ET']:
                ListeCSV[-1].append(i)
            ListeCSV[-1].append('FINET') 
            ListeCSV[-1].append(dico['Question']) 
            for i in dico['REP']:
                ListeCSV[-1].append(i)
            ListeCSV[-1].append('FINREP')
            for i in dico['BREP']:
                ListeCSV[-1].append(i)
        with open(PATH,'w',newline='') as FILE:
            Ecriture=csv.writer(FILE,delimiter=';')  
            #print(ListeCSV)      
            Ecriture.writerows(ListeCSV)
        FILE.close()
        return True
    else:
        return False

#modif_csv(1,{'ID':'3','Question': 'machin', 'ET': ['Info'], 'REP': ['truc', 'bidule', '4','5'], 'BREP': ['4']})

def delQuestion(ID_User,IDquestion):
    """
    Procédure: donc pas de sortie
    Entrée:ID_User=> id de l'utilisateur
            IDquestion=> id de la question à supprimer
    Tâche effectuer:Supprime la question ayant la même id que IDquestion.
    On doit réécrire en intégralité le fichier
    """
    PATH= os.getcwd()
    PATH =  PATH+littlePATH+"/question_"+str(ID_User)+".csv"
    if (os.path.isfile(PATH)):
        lecture = depuis_csv(ID_User)
        ListeCSV=[]
        for dico in lecture:        
            if (dico['ID']!=str(IDquestion)):
                    ListeCSV.append([])
                    ListeCSV[-1].append(dico['ID'])
                    for i in dico['ET']:
                        ListeCSV[-1].append(i)
                    ListeCSV[-1].append('FINET') 
                    ListeCSV[-1].append(dico['Question']) 
                    for i in dico['REP']:
                        ListeCSV[-1].append(i)
                    ListeCSV[-1].append('FINREP')
                    for i in dico['BREP']:
                        ListeCSV[-1].append(i)
        with open(PATH,'w',newline='') as FILE:
            Ecriture=csv.writer(FILE,delimiter=';')  
            #print(ListeCSV)      
            Ecriture.writerows(ListeCSV)
        FILE.close()
    PATH= os.getcwd()
    PATH =  PATH+littlePATH+"/ID_Question"+".csv"
    with open(PATH,"r") as FILE:
        lecture=csv.reader(FILE,delimiter=";")
        li=[]
        for i in lecture:
            if(i[0]!=IDquestion):
                li.append(i)
        with open(PATH,"w") as FILE2:
            Ecriture=csv.writer(FILE2,delimiter=';')
            Ecriture.writerows(li)

#delQuestion(1,4)

def getQuestion(ID_User,IDquestion):
    """
    Entrée:ID_User => id de l'utilisateur   
           IDquestion => id de la question
    Sortie: dictionnaire de la question d'id IDquestion de l'utilisateur d'id ID_User
    """
    liste = depuis_csv(ID_User)
    for dico in liste:
        if (dico['ID']==str(IDquestion)):
            return dico
#print(getQuestion(1,1))