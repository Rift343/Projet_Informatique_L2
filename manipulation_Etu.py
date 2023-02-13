import csv
import os
import markdownHTML
import hashlib
littlePATH = "/csv"

def etuCSV():
    """
    Entrée: Rien
    sortie:Liste de liste de string décrivant les étudiants.
    Principe: Comme pour lireCSV(). On va lire le fichier csv ligne par ligne 
    afin de récupérer tout les étudiants ainsi que leurs informations
    """
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"/Etu.csv"
    with (open(PATH,'r')) as FILE:
        lecture = csv.reader(FILE,delimiter=';')
        listeEtu = list()
        for i in lecture:
            listeEtu.append(i)
        #os.close(FILE)
    return listeEtu


def ajoutEtu(fichierCSV):
    """
    Entrée:Le liens vers un ficher csv
    Sortie:Un boolean true
    Principe:On va lire dans fichierCSV la liste des etudiants puis ouvrir le fichier de 
    stockage de l'ensemble des étudiants en append ('a') ensuite l'on ecrit nom, prenom, 
    numéro etuduant et mdp. 
    """
    PATH = os.getcwd()
    fichierCSV = PATH +'/'+fichierCSV
    print(fichierCSV)
    with open(fichierCSV,'r') as FILE:
        lecture=csv.reader(FILE,delimiter=';')
        PATH=os.getcwd()
        PATH = PATH+littlePATH+"/Etu.csv"
        with (open(PATH,'a',newline='')) as FILE2:
            Ecriture = csv.writer(FILE2,delimiter=';')
            for i in lecture:
                mdp = i[-1]
                i.append(hashlib.sha256(mdp.encode()).hexdigest())
                Ecriture.writerow(i)
            #os.close(FILE2)
        #os.close(FILE)
    
    os.remove(fichierCSV)
    return True
                
def modificationEtu(numeroEtu,password):
    """
    Entré: numeroEtu-> le numéro de l'étudiant où l'on veut modifier le mot de passe
            password-> le nouveau password sans le hash
    Sortie: Rien
    Principe: On lit le fichier des étudiants, on fait la modificaiton du password au bon étudiant
              Puis l'on réécrit tout le ficher csv avec les modification
    """
    listeEtudiant = etuCSV()
    print(listeEtudiant)
    for i in range (len(listeEtudiant)):
        if (listeEtudiant[i][2]==numeroEtu):
            password = hashlib.sha256(password.encode()).hexdigest()
            listeEtudiant[i][3] = password
    PATH = os.getcwd()
    PATH=PATH+littlePATH+"/Etu.csv"
    with open(PATH,'w') as FILE:
        Ecriture = csv.writer(FILE,delimiter=';')
        Ecriture.writerows(listeEtudiant)
        #os.close(FILE)

def ajouterHistoEtu(listeDeLaRep,numEtu):
    """
    Entré: listeDeLaRep=>Liste correspondant au élement de la réponse format à définir
            numEtu=> Numéro de l'étudiant dans lequel on veut ajouter un historique
    Sortie:Rien
    Principe: On va transformer listeDeLaRep en string puis on va vérifier que la réponse 
    n'existent pas déja dans l'historique. Puis on fait la modification dans Etu.csv
    """
    RepStr = "@||||@".join([str(elem)for elem in listeDeLaRep])
    PATH=os.getcwd()
    PATH=PATH+littlePATH+"/Etu.csv"
    listeEtu = etuCSV()
    monBoolean = True
    for i in range(len(listeEtu)):
        if (listeEtu[i][2]==str(numEtu)):
            for x in range(4,len(listeEtu[i])):
                #print(listeEtu[i][x])
                if(listeEtu[i][x]==RepStr):
                    monBoolean=False
            if monBoolean:
                listeEtu[i].append(RepStr)
    with open(PATH,'w',newline='') as FILE:
        Ecriture = csv.writer(FILE,delimiter=';')
        for etu in listeEtu:
            Ecriture.writerow(etu)



#print(etuCSV())

def GetHistoEtu(numEtu):
    """
    Entrée:numEtu=>numero de l'étudiant 
    Sortie:Une de liste de liste de string
    Principe: On lit la liste des etudiants. 
    Lorsque l'on à trouver l'étudiant qui nous intéresse alors on récupère sont historique
    en supprimant les delimiter que l'on avait ajouter afin d'avoir une liste de liste de string
    qui correspond au réponse
    """
    listeEtu=etuCSV()
    listeRetour=[]
    for i in listeEtu:
        if (i[2]==str(numEtu)):
            for y in range(4,len(i)):
                listeRetour.append(i[y].split("@||||@"))
    return listeRetour

#ajouterHistoEtu(["JE","suis","une","liste"],1258)
#ajouterHistoEtu(["JE","suis","une","autre","liste"],1258)
#print(GetHistoEtu(1258))