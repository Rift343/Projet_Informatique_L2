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
    O(n)+O(n²) donc O(n²) car depuis_csv est en O(n²)
    """
    listeDeRetour=[]
    listeDesQuestion=manipulationQuestion.depuis_csv(ID_User)
    for element in listeDesQuestion:
        if Eti in element['ET']:
            listeDeRetour.append(element['ID'])
    return listeDeRetour


def TraitementIntervalle(nbtotaleQuestion,traitementIntervalle,listeIntervalle,tailleExam=0):
    """
    O(n) * 3(m) donc O(n*m) cependant cela revient à faire O(n²)
    """
    tailleExam = 0
    while tailleExam < nbtotaleQuestion:
         #   print("2")
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
    return listeIntervalle,traitementIntervalle



def creer_sujet(ListeEtiquette,listeIntervalle,nbSujet,ID_User,nbtotaleQuestion,melange):
    liste_sujet=[]
    erreur =False
    sauveguardeListeIntervalle = []
    for i in listeIntervalle:
        sauveguardeListeIntervalle.append(i)
    #print(sauveguardeListeIntervalle)
    while len(liste_sujet)<nbSujet:#n
        #print("1")
        #liste_sujet.append(1)
        
        traitementIntervalle=[]
        for i in range(len(listeIntervalle)):
            traitementIntervalle.append(0)
        #print (traitementIntervalle)
        
        #####################################
        listeIntervalle,traitementIntervalle =TraitementIntervalle(nbtotaleQuestion,traitementIntervalle,listeIntervalle)#n² donc n^3 avec le while

        #print('ok')
        #print("sauva=",sauveguardeListeIntervalle)
        #print(traitementIntervalle) 
        
        listeIntervalle = []
        for z in sauveguardeListeIntervalle:#n donc n² avec le while
            listeIntervalle.append(z)

        
        #print("sauve =",listeIntervalle) 
        newSujet,erreur =creation1sujet(ListeEtiquette,ID_User,traitementIntervalle)#n^3 donc n^4 avec la boucle while
        #print(newSujet)
        #print(newSujet)
        #print("2.5")
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
        nouvelle_code_err=False
        #print(liste_sujet_sort)
        while (newSujetSort in liste_sujet_sort):

            traitementIntervalle=[]
            for i in range(len(listeIntervalle)):#n^3
                traitementIntervalle.append(0)
            #print (traitementIntervalle)
        
            #####################################
            listeIntervalle,traitementIntervalle =TraitementIntervalle(nbtotaleQuestion,traitementIntervalle,listeIntervalle)#O(n^4) avec les deux while

            #print('ok')
            #print("sauva=",sauveguardeListeIntervalle)
            #print(traitementIntervalle) 
        
            listeIntervalle = []
            for z in sauveguardeListeIntervalle:
                listeIntervalle.append(z)



                    
            #print("3")
            newSujet,nouvelle_code_err=creation1sujet(ListeEtiquette,ID_User,traitementIntervalle)#n^3 donc n^5 avec les boucle while
            #print(liste_sujet_sort)
            #print(newSujet)
            compteur=compteur+1
            erreur = erreur or nouvelle_code_err
            if (compteur==1000):
                return liste_sujet,True
            newSujetSort=copy.deepcopy(newSujet)
        #print(newSujetSort)
            newSujetSort.sort()
        liste_sujet.append(newSujet)
    return liste_sujet,False
    #Au finale cette algorithme est en O(n^5) il ne fait oublié qui il y a beaucoup de O(n²),O(n^3) et O(n^4)
        
            

def creation1sujet(ListeEtiquette, ID_User,traitementIntervalle):
    """
    O(n^3) car on fait n fois recupererListeQuestionParEtiquette qui et en n²
    """
    newSujet=[]
    erreur=False
    for i in range (len(ListeEtiquette)):#n
            nombreElement=traitementIntervalle[i]
            sujetDispo = recupererListeQuestionParEtiquette(ID_User,ListeEtiquette[i])#n²
            for y in range(nombreElement):#n
                #print(sujetDispo)
                question =random.choice(sujetDispo)
                #print("sujetdispo : ",sujetDispo)
                #print("sujet chois : ",question)
                #print((newSujet))
                #print((set(sujetDispo)-set(newSujet)!=set()))
                
                while (question in newSujet) and (set(sujetDispo)-set(newSujet)!=set()):#n
                    #print("boucle")
                    #print(question,newSujet,sujetDispo)
                    #print(set(sujetDispo)-set(newSujet))
                    question =random.choice(sujetDispo)
                if(set(sujetDispo)-set(newSujet)==set()):
                    erreur = True
                #print("hit")
                sujetDispo.remove(question)
                #print("hit2")
                #print("newsujet avant append",newSujet)
                newSujet.append(question)
                #print("newsujet apres append",newSujet)
                #print("hit3")
    #print(newSujet)
    return newSujet,erreur
    


        



#liste1=creer_sujet(["QCM"],[[1,2]],4,"ba31fDpm",2,True)
#print(liste1)
#print((recupererListeQuestionParEtiquette("ba31fDpm","QCM")))
