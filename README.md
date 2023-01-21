# Projet_Informatique_L2
Ceci est le dépot du code d'un projet d'informatique de licence 2 à l'Université de Montpellier

# Consigne d'installation:

1- Installer flask celon votre platforme :https://flask.palletsprojects.com/en/2.2.x/installation/#install-flask <br/>
2-Installer la bibliothèque Markdown avec la commande:pip install mardown <br/>
3-Télécharger le code source. Les autres bibliothèques sont présentes sous forme de ficher source à l'intérieur. <br/>
# Consigne de Lancement:

1-Dans le code source il y a un ficher nommé serveur.py. Vous devez lancer se fichier,nous utilisons Visual Studio Code et VS codium pour nos test. <br/>
2-Ouvrer votre navigateur web et entre l'addresse localhost:5000 (Google Chorme,Mozilla Firefox,Microsoft EDGE et CCleaner Browser fonctionne) <br/>
3-Vous pouver alors utiliser le site comme vous le voulez. <br/>
4-Enfin pour finir le processus CTRL+C dans le console de commande de visual Studio. <br/>

# Format des fichers .csv

Afin de garder les informations entre les différentes utilisations du serveur, nous utilisons des fichiers CSV. Vous trouverez au total deux types de fichier CSV:

## Le fichier csv contenant les utilisateurs

Ce fichier garde différente information sur les utilisateurs sous le format ci-dessous: <br/>
ID_User;NOM;EMAIL;password

## Les fichiers csv contenant les questions des utilisateurs

Ces fichiers sont nommés en fonction de l'ID de l'utilisateur. Par exemple le fichier des questions de l'utilisateur 143 se nommera question_143.csv.<br/>
Ils respectent le format ci-dessous:<br/>
ET=étiquette REP=réponse BREP=Bonne réponse<br/>
Id;ET1;ET2;ET3;...;FINET;Question;REP1;REP2;...;FINREP;BREP1;BREP2;...<br/>


