import csv
import os

littlePATH = "\\test"

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
    PATH = PATH+littlePATH+"\question_"+str(ID_User)+".csv"#Au modifié pour correspondre dès que les csv seront changés de répertoires
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
            print(ligne)
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

def estDansCSV(ID_User,ID_Question):
    maliste = depuis_csv(ID_User)
    for i in maliste:
        if (i['ID']==ID_Question):
            return False
    return True


def doublon(ID_User,Question,reponse):
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
    ListeCSV=list()
    PATH= os.getcwd()
    PATH =  PATH+littlePATH+"\question_"+str(ID_User)+".csv"#Au modifié pour correspondre dès que les csv seront changés de répertoires
    if(os.path.isfile(PATH)):
        id=1
        while (estDansCSV(ID_User,str(id))==False):
            id = id + 1
            print(id)
        ListeCSV.append(id)
        if doublon(ID_User,Dico_csv['Question'],Dico_csv['REP']):
            return False
          
    else:
        id=1
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

    print(ListeCSV)
    with open(PATH,'a',newline='') as FILE:
        Ecriture=csv.writer(FILE,delimiter=';')   
        Ecriture.writerow(ListeCSV)
        FILE.close() 

dans_csv(1,{'Question': 'Nb Ocet INT', 'ET': ['Info'], 'REP': ['2', '3', '4','5'], 'BREP': ['4']})     


