from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

@app.route("/") #Page principale du site
def index():
    return render_template("html/welcome.html")

@app.route("/register") #Page de création d'un compte
def reg():
    return render_template("html/register.html")

@app.route("/login") #Page de connexion à un compte
def log():
    return render_template("html/login.html")

@app.route("/BDD") #Page d'accueil du compte avec la vue de toutes les questions créées et les étiquettes en haut, lorsqu'on clique sur une étiquette on ne voit plus que
def BDD():          #les questions qui ont cette étiquette
    return render_template("html/BDD.html")


@app.route("/creationQuestion") #Page de création d'une question avec un nom, un énoncé, des réponses, une correction et des étiquettes
def creationQuestion():
    return render_template("html/creationQuestion.html")

@app.route("/creationQuestion",methods = ['POST']) #Code d'enregistrement d'une question une fois que toutes ses infos ont été rentrées pour une création
def ajoutQuestion():
    #idQuestion #= #il faudrait rajouter ici un identifiant de question pas encore utilisé
    name = request.form['name'] #On récupère le nom de la question
    enonce = request.form['enonce'] #Son énoncé
    reponses = request.form['reponses'] #Ses réponses
    correction = request.form['correction'] #Sa correction
    etiquettes = request.form['etiquettes'] #Ses étiquettes
    idUser = request.form['idUser'] #L'id de l'utilisateur qui ajoute la question // je pense pas qu'on le récupère dans le form
    #file1 = open("question.csv","a") #On ouvre le fichier csv où la question doit être enregistrée
    #string = name+'///'+enonce+'///'+str(reponses)+'///'+str(correction)+'///'+str(etiquettes)+'\n' #On créée la ligne qui sera enregistrée en append avec '///' comme séparateur (temporaire)
    #file1.write(string) #On écrit la ligne dans le fichier
    #return render_template("html/question/"+idQuestion+".html") #On renvoie la personne sur la vue de la question créée (si elle a bien été créée)

@app.route("/question/<idQuestion>") #Page de visualisation d'une question
def creationQuestion(idQuestion):
    return render_template("html/"+idQuestion+".html")

@app.route("/modificationQuestion/<idQuestion>") #Page de modification d'une question
def modifierQuestion(idQuestion):
    return render_template("html/modificationQuestion/"+idQuestion+".html") #pour la modification il faut récupérer les infos existantes de la question et refaire la même chose qu'à la création

@app.route("/modificationQuestion/<idQuestion>",methods = ['POST']) #Code d'enregistrement d'une question une fois que toutes ses infos ont été rentrées pour une modif
def modificationQuestion(idQuestion):
    name = request.form['name'] #On récupère le nom de la question
    enonce = request.form['enonce'] #Son énoncé
    reponses = request.form['reponses'] #Ses réponses
    correction = request.form['correction'] #Sa correction
    etiquettes = request.form['etiquettes'] #Ses étiquettes
    idUser = request.form['idUser'] #L'id de l'utilisateur qui ajoute la question // je pense pas qu'on le récupère dans le form
    #file1 = open("question.csv","a") #On ouvre le fichier csv où la question doit être enregistrée
    #string = name+'///'+enonce+'///'+str(reponses)+'///'+str(correction)+'///'+str(etiquettes)+'\n' #On créée la ligne qui sera enregistrée en append avec '///' comme séparateur (temporaire)
    #Ici on peut pas juste écrire dans le fichier, il faut soit réecrire sur la question existante soit supprimer la question existante et écrire la nouvelle (ou atre méthode ?)
    #return render_template("html/question/"+idQuestion+".html")


@app.route("/creationFeuille") #Page de création d'une feuille de questions
def creationFeuille():
    return render_template("html/creationFeuille.html")

@app.route("/creationFeuille",methods = ['POST']) #La création d'une feuille 
def feuille():
    return render_template("html/feuille.html")

#@app.route("/feuille")
#def feuille():
#    return render_template("feuille.html")


@app.route("/css/<nomcss>")
def recuperationCSS(nomcss):
    return render_template("css/"+nomcss+".css")