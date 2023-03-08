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

def dicoPourFaciliteLesStat(ID_User):
    """
    Lit l'historique est le formate pour renvoyer un dictionnaire de
    """
    Historique= lireHisto(ID_User)
    DicoQuestionDirect={}
    DicoQuestionSeq={}
    for question in Historique:
        for reponse in question[1:]:
            #print (reponse[2])
            if reponse[3]=='Sequence':
                #print("OK")   
                #print(question[0]+"seq"+reponse[3] in DicoQuestionSeq)             
                if(question[0]+"seq"+reponse[4] in DicoQuestionSeq ):
                    DicoQuestionSeq[question[0]+"seq"+reponse[4]].append(reponse)
                else:
                    DicoQuestionSeq[question[0]+"seq"+reponse[4]] = [reponse]
                    #print("init")
                    #print(DicoQuestionSeq)
            if reponse[3]=="Direct":
                if(question[0] in DicoQuestionDirect):
                    DicoQuestionDirect[question[0]].append(reponse)
                else:
                    DicoQuestionDirect[question[0]] = [reponse]
    #print(DicoQuestionDirect)
    #print(DicoQuestionSeq)
    return DicoQuestionDirect,DicoQuestionSeq
                
def nbPositive(Dico):
    """
    Entré:Un dico d'historique
    Sortie:Une dictionnaire dont les clé est l'id de la question
    (pour les séquences c'est idquestion+seq+idseq) et ayant pour valeur un couple
    représentant le pourcentage de réponse positive et le nb de réponse totale
    """
    DicoNB={}
    for key in Dico:
        DicoNB[key]=len(Dico[key])
        compteur=0
        #print(key)
        for element in Dico[key]:
            #print(element)
            if element[1]=='Vrai':
                compteur=compteur+1
        if compteur==0:
            DicoNB[key] = (0,DicoNB[key])
        else :
            DicoNB[key] = ((compteur/DicoNB[key])*100,DicoNB[key])
    return DicoNB

def nbUserHisto(dicoHisto):
    """
    Entré: Un dico d'historique
    Sortie: Une dictionnaire dont les clé est l'id de la question
    (pour les séquences c'est idquestion+seq+idseq) et ayant pour valeur le nombre
    d'élève différent qui on répondu
    """
    DicoNB={}
    for key in dicoHisto:
        DicoNB[key]=0
        liste=[]
        for element in dicoHisto[key]:
            if not( element[2] in liste):
                liste.append(element[2])
                DicoNB[key]=DicoNB[key]+1            
    #print(DicoNB)
    return(DicoNB)

def supprimerUneQuestion(Liste,ID_Users,ID_Question):
    """
    Entré: liste de type[date,Vrai ou Faux,idetu,Sequence ou direct,id sequence]
    Id de l'utilisateur(prof), id de la question à laquelle on veut supprimer l'historique
    Tache: supprimer un réponse à une question
    """
    historique = lireHisto(ID_Users)
    for i in range (len(historique)):
        if str(historique[i][0]) == str(ID_Question):
            historique[i].remove(Liste)
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"/historique_"+str(ID_Users)+".csv"
    os.remove(PATH)   
    for i in historique:
        for y in range(1,len(i)):
            #print(ID_Users,i[0],i[y])
            ajouterHisto(ID_Users,i[0],i[y])    


"""
ajouterHisto(1,1,["Jour/moi/annes","Juste ou Faux","idEtu","Direct ou Sequence","identifiant de la seq"])
ajouterHisto(1,1,["22/09/76","Faux","ve","Direct"])
ajouterHisto(1,2,["07/04/2003","Vrai","ve","Sequence","76"])
ajouterHisto(1,2,["07/04/2003","Vrai","ae","Direct"])
ajouterHisto(1,2,["07/04/2003","Vrai","ve","Sequence","67"])
ajouterHisto(1,2,["07/04/2003","Vrai","ae","Sequence","7o"])
ajouterHisto(1,2,["07/04/2003","Vrai","ae","Sequence","76"])
ajouterHisto(1,2,["07/04/2003","Faux","ae","Sequence","76"])
ajouterHisto(1,2,["07/04/2003","Faux","ea","Sequence","76"])
ajouterHisto(1,2,["07/04/2003","Faux","ve","Sequence","76"])
#print(lireHisto(1))
dicoPourFaciliteLesStat(1)
DicoDirect,DicoSeq =dicoPourFaciliteLesStat(1)
Nombre_de_Pos=nbPositive(DicoSeq)
Nombre_de_Pos2=nbPositive(DicoDirect)
print("Nombre de reponse positive au sequence",Nombre_de_Pos)
print("Nombre de reponse positive des question en direct : ",Nombre_de_Pos2)
print("Nb de participant au séquence : ",nbUserHisto(DicoSeq))
print("Nb de participant au question en direct : ", nbUserHisto(DicoDirect))
#supprimerUneQuestion(["07/04/2003","Faux","ve","Sequence","76"],1,2)
#print(lireHistoQuestion(1,4))"""