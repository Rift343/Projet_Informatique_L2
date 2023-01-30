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
    return listeEtu


def ajoutEtu(fichierCSV):
    """
    Entrée:Le liens vers un ficher csv
    Sortie:Un boolean true
    Principe:On va lire dans fichierCSV la liste des etudiants puis ouvrir le fichier de 
    stockage de l'ensemble des étudiants en append ('a') ensuite l'on ecrit nom, prenom, 
    numéro etuduant et mdp. 
    """
    with (open(fichierCSV),'r') as FILE:
        lecture=csv.reader(FILE,delimiter=';')
        PATH=os.getcwd()
        PATH = PATH+littlePATH+"/Etu.csv"
        with (open(PATH,'a',newline='')) as FILE2:
            Ecriture = csv.writer
            for i in lecture:
                mdp = i[-1]
                i.append(hashlib.sha256(mdp.encode()).hexdigest(),delimiter=';')
                Ecriture.writerow(i)
    return True
                