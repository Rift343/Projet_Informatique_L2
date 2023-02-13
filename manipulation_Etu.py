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

