import manipulationQuestion
import random
import copy

def recupererListeQuestionParEtiquette(ID_User,Eti):
    """
    Entre: ID_User => Identidiant de l'utilisateur(string)
           Eti => Etiquette (String)
    Retour:Liste des id des questions ayant pour etiquette eti
    Principe: On récupére les dictionnaires de toute les questions d'un professuer
    puis on le parcours, chaque questions possedant l'étiquette eti sera ensuite
    ajouter à la liste de retour
    """
    listeDeRetour=[]
    listeDesQuestion=manipulationQuestion.depuis_csv(ID_User)
    for element in listeDesQuestion:
        if Eti in element['ET']:
            listeDeRetour.append(element['ID'])
    return listeDeRetour

def creer_sujet(ListeEtiquette,listeIntervalle,nbSujet,ID_User,nbtotaleQuestion):
    liste_sujet=[]
    sauveguardeListeIntervalle = []
    for i in listeIntervalle:
        sauveguardeListeIntervalle.append(i)
    #print(sauveguardeListeIntervalle)
    while len(liste_sujet)<nbSujet:
        #liste_sujet.append(1)
        
        traitementIntervalle=[]
        for i in range(len(listeIntervalle)):
            traitementIntervalle.append(0)
        #print (traitementIntervalle)
        tailleExam = 0
        while tailleExam < nbtotaleQuestion:
            for y in range (len(listeIntervalle)):
                #print(listeIntervalle)
                traitementIntervalle[y]=listeIntervalle[y][0]
                tailleExam = tailleExam + listeIntervalle[y][0]
                listeIntervalle[y] =listeIntervalle[y][1] - listeIntervalle[y][0] 
            #print(traitementIntervalle)
            #print("liste ",listeIntervalle)
            for z in range(len(listeIntervalle)):
                value = random.randrange(0,listeIntervalle[z]+1)
                if (tailleExam+value<=nbtotaleQuestion):
                    #print(value)
                    tailleExam = tailleExam+value
                    traitementIntervalle[z]=traitementIntervalle[z]+value
                    listeIntervalle[z] =listeIntervalle[z] - value
            #print(traitementIntervalle)
            #print(listeIntervalle)
            for z in range(len(listeIntervalle)):
                if (listeIntervalle[z]!=0):
                    for x in range(listeIntervalle[z]):
                        if (tailleExam+1<=nbtotaleQuestion):
                            tailleExam=tailleExam+1
                            traitementIntervalle[z]=traitementIntervalle[z]+1
                            listeIntervalle[z] =listeIntervalle[y] - 1
        #print('ok')
        #print("sauva=",sauveguardeListeIntervalle)
        #print(traitementIntervalle) 
        listeIntervalle = []
        for z in sauveguardeListeIntervalle:
            listeIntervalle.append(z)

        
        #print("sauve =",listeIntervalle) 
        newSujet=creation1sujet(ListeEtiquette,ID_User,traitementIntervalle)
        #print(newSujet)
        #print(newSujet)
        newSujetSort=copy.deepcopy(newSujet)
        #print(newSujetSort)
        newSujetSort.sort()
        #print(newSujetSort)
        #print(newSujet)
        #print(listeIntervalle)
        liste_sujet_sort =copy.deepcopy(liste_sujet)
        for i in range (len(liste_sujet_sort)):   
            liste_sujet_sort[i].sort()

        compteur=0
        while (newSujetSort in liste_sujet_sort):
            newSujet=creation1sujet(ListeEtiquette,ID_User,traitementIntervalle)
            compteur=compteur+1
            if (compteur==1000):
                return liste_sujet
        liste_sujet.append(newSujet)
    return liste_sujet
        
            

def creation1sujet(ListeEtiquette, ID_User,traitementIntervalle):
    newSujet=[]
    for i in range (len(ListeEtiquette)):
            nombreElement=traitementIntervalle[i]
            sujetDispo = recupererListeQuestionParEtiquette(ID_User,ListeEtiquette[i])
            for y in range(nombreElement):
                question =random.choice(sujetDispo)
                while question in newSujet:
                    question =random.choice(sujetDispo)
                sujetDispo.remove(question)
                newSujet.append(question)
    return newSujet
    
  

        



print(creer_sujet(["test","QCM"],[[1,1],[2,3]],10,"ba31fDpm",4))
#print((recupererListeQuestionParEtiquette("ba31fDpm","QCM")))
