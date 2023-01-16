import csv
import os

def depuis_csv(ID_User):
    """
    Ouvre un fichier au format csv
    """    
    PATH = os.getcwd()
    PATH = PATH+"\\test\question_"+str(ID_User)+".csv"
    with open(PATH,'r') as FILE:
        lecture=csv.reader(FILE,delimiter=';')
        ListeQuestion=[]
        for ligne in lecture:
            ListeQuestion.append(ligne)
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