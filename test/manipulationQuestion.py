import csv
import os

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
    PATH = PATH+"\\test\question_"+str(ID_User)+".csv"#Au modifié pour correspondre dès que les csv seront changés de répertoires
    #On ajoute au PATH le chemin vers notre fichier 
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
    


depuis_csv(1)