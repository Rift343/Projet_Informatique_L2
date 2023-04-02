import csv
import os
from random import randrange

littlePATH = "/csv"


def lireCSV():
    """
    Sortie: Liste de liste de string correspondant au l'intégralité des utilisateurs 
    Principe: On va lire le ficher contenant les utilisateurs puis on va écrire ce fichier
    dans un liste que l'on renvoie
    """
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"/User.csv"
    with open(PATH, 'r') as FILE:
        lecture = csv.reader(FILE, delimiter=';')
        ListeUSER = []
        for i in lecture:
            ListeUSER.append(i)
    return ListeUSER


# print(lireCSV())

def ajouterUser(Nom, password, email):
    """
    Entrée: trois string Nom, password,email
    Sortie un boolean True
    Principe: L'on récupère la liste des utilisateurs existants puis 
    on vérifie si le mot de passe et l'email sont unique et on donne
    le plus petit nombre possible unique pour être l'identifiant.
    Enfin on écrit notre nouvel utilisateur dans le fichier des utilisateur
    """
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"/User.csv"
    listeUSER = lireCSV()
    listeid = []
    for user in listeUSER:
        listeid.append(user[0])
        if (password == user[3] or email == user[2] or Nom == user[1]):
            return False

    with open(PATH, 'a', newline='') as FILE:
        li = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e",
              "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        id = "EA167PM8"
        #print (id)
        #print (listeid)
        #print(id in listeid)
        while (str(id) in listeid):
            id = ""
            for i in range(8):
                id = id+li[randrange(len(li))]
        Ecriture = csv.writer(FILE, delimiter=';')
        Ecriture.writerow([id, Nom, email, password])

    return True

# print(ajouterUser("hiu","bj","bui@yahoo.com"))
