import csv
import os

littlePATH = "\\test"

def lireCSV():
    """
    Sortie: Liste de liste de string correspondant au l'intégralité des utilisateurs 
    Principe: On va lire le ficher contenant les utilisateurs puis on va écrire ce fichier
    dans un liste que l'on renvoie
    """
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"\\testUser.csv"
    with open(PATH,'r') as FILE:
        lecture = csv.reader(FILE,delimiter=';')
        ListeUSER=[]
        for i in lecture:
            ListeUSER.append(i)
    return ListeUSER
            

#print(lireCSV())

def ajouterUser(Nom,password,email):
    """
    Entrée: trois string Nom, password,email
    Sortie un boolean True
    Principe: L'on récupère la liste des utilisateurs existants puis 
    on vérifie si le mot de passe et l'email sont unique et on donne
    le plus petit nombre possible unique pour être l'identifiant.
    Enfin on écrit notre nouvel utilisateur dans le fichier des utilisateur
    """
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"\\testUser.csv"
    listeUSER = lireCSV()
    listeid=[]
    for user in listeUSER:
        listeid.append(user[0])
        if (password==user[3] or email==user[2] ):
            return False
    
    with open(PATH,'a',newline='') as FILE:
        id = 1
        print (id)
        print (listeid)
        print(id in listeid)
        while (str(id) in listeid):
            id = id +1
        Ecriture=csv.writer(FILE,delimiter=';')   
        Ecriture.writerow([id,Nom,email,password])      
        
    return True

#print(ajouterUser("Jaque","JE","vneiu@gmail.com"))


    
