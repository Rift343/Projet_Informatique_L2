import csv
import os

littlePATH = "\\test"

def lireCSV():
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"\\testUser.csv"
    with open(PATH,'r') as FILE:
        lecture = csv.reader(FILE,delimiter=';')
        ListeUSER=[]
        for i in lecture:
            ListeUSER.append(i)
    return ListeUSER
            

print(lireCSV())

def ajouterUser(Nom,password,email):
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
        while (id in listeid):
            id = id +1
        Ecriture=csv.writer(FILE,delimiter=';')   
        Ecriture.writerow([id,Nom,email,password])      
        
    return True

print(ajouterUser("Jaque","MDP","Jaque@gmail.com"))


    
