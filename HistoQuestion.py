import csv
import os
littlePATH = "/csv"

def lireHistoQuestion(ID_User,IdQuestion):
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"/historique_"+str(ID_User)+".csv"
    if(not(os.path.isfile(PATH))):
        return []
    with open(PATH,'r') as FILE:
        lecture=csv.reader(FILE,delimiter=';')
        for ligne in lecture:
            if ligne[0] == str(IdQuestion):
                listeRetour=[]
                for i in range(1,len(ligne)):
                    listeRetour.append(ligne[i].split("@||||@"))
                return listeRetour
    return []


def lireHisto(ID_User):
    ListeRetour=[]
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"/historique_"+str(ID_User)+".csv"
    if(not(os.path.isfile(PATH))):
        return []
    with open(PATH,'r') as FILE:
        lecture=csv.reader(FILE,delimiter=';')
        for ligne in lecture:
            histo=ligne
            for i in range(1,len(ligne)):
                histo[i]=histo[i].split("@||||@")
            ListeRetour.append(ligne)
    return ListeRetour

def ajouterHisto(ID_User,IdQuestion,histo):
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"/historique_"+str(ID_User)+".csv"
    if (lireHistoQuestion(ID_User,IdQuestion)!=[]):
        listeHistorique=lireHisto(ID_User)
        index=0
        for i in range(0,len(listeHistorique)):
            if(listeHistorique[i][0] == str(IdQuestion)):
                index = i
        listeHistorique[index].append(histo)
        for y in range(0,len(listeHistorique)):
            for x in range(1,len(listeHistorique[y])):
                listeHistorique[y][x]="@||||@".join([str(elem)for elem in listeHistorique[y][x]])
        with open(PATH,'w',newline='') as FILE:
            Ecriture = csv.writer(FILE,delimiter=';')
            Ecriture.writerows(listeHistorique)
    else:
        with open(PATH,'a',newline='') as FILE:
            Ecriture=csv.writer(FILE,delimiter=';')
            Ecriture.writerow([IdQuestion,"@||||@".join([str(elem)for elem in histo])])

#ajouterHisto(1,1,[1,2,3])
#ajouterHisto(1,1,[1,2,4])
#ajouterHisto(1,2,[1,2,4])
#ajouterHisto(1,3,[1,2,4])
#ajouterHisto(1,3,[1,"vbreu",4])
#print(lireHisto(1))
#print(lireHistoQuestion(1,4))