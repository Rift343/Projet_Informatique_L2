import csv
import os
from random import randrange
littlePATH = "/csv"


def lireSequence(ID_User, ID_Sequence):
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"/Sequence_"+str(ID_User)+".csv"
    if (not (os.path.isfile(PATH))):
        return []
    with open(PATH, 'r') as FILE:
        lecture = csv.reader(FILE, delimiter=';')
        for ligne in lecture:
            if ligne[0] == ID_Sequence:
                return ligne[1:]
    return []


def lireSequenceUser(ID_User):
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"/Sequence_"+str(ID_User)+".csv"
    if (not (os.path.isfile(PATH))):
        return []
    with open(PATH, 'r') as FILE:
        lecture = csv.reader(FILE, delimiter=';')
        liste = list()
        for ligne in lecture:
            liste.append(ligne)
        return liste


def listeSequence():
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"/IdSequence"+".csv"
    if (not (os.path.isfile(PATH))):
        return [[]]
    with open(PATH, 'r') as FILE:
        lecture = csv.reader(FILE, delimiter=';')
        liste = []
        for ligne in lecture:
            liste.append(ligne)
    return liste


def ajouterSequence(ID_User, listeIdQuestion):
    id = "1TV98Bey"
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"/Sequence_"+str(ID_User)+".csv"
    with open(PATH, 'a', newline='') as FILE:
        Ecriture = csv.writer(FILE, delimiter=';')
        li = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e",
              "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        # print(listeSequence())
        while (str(id) in listeSequence()[0]):
            # print(id)
            id = ""
            for i in range(8):
                id = id+li[randrange(len(li))]
        listeIdQuestion.insert(0, id)
        Ecriture.writerow(listeIdQuestion)
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"/IdSequence"+".csv"
    with open(PATH, 'a', newline='') as FILE:
        Ecriture = csv.writer(FILE, delimiter=';')
        Ecriture.writerow([id])


def modifierSequence(ID_User, IdSequence, ListeSequence):
    PATH = os.getcwd()
    PATH = PATH+littlePATH+"/Sequence_"+str(ID_User)+".csv"
    sequence = lireSequenceUser(ID_User)
    # print(sequence)
    for i in range(0, len(sequence)):
        # print(sequence[i][0])
        if str(sequence[i][0]) == str(IdSequence):
            print('OK')
            sequence2 = [IdSequence]
            for t in ListeSequence:
                sequence2.append(t)
            sequence[i] = sequence2
    with open(PATH, 'w', newline='') as FILE:
        Ecriture = csv.writer(FILE, delimiter=';')
        Ecriture.writerows(sequence)


# ajouterSequence("FTTYH",[1,2,3])
# ajouterSequence("FTTYH",[1,"fbej",3])
# ajouterSequence("FTTYH",[1,2,"vbejh"])
# modifierSequence("FTTYH","1TV98Bey",['test,test',1])
