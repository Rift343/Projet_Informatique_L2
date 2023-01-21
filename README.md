# Projet_Informatique_L2

Ceci est le dépot du code d'un projet d'informatique de licence 2 à l'Université de Montpellier

# Consignes d'installation:

1 - Installez flask selon votre plate-forme : https://flask.palletsprojects.com/en/2.2.x/installation/#install-flask <br/>
2 - Installez la bibliothèque Markdown avec la commande : pip install markdown <br/>
3 - Téléchargez le code source. Les autres bibliothèques sont présentes sous forme de ficher source à l'intérieur. <br/>

# Consignes de lancement:

1 - Dans le code source il y a un fichier nommé serveur.py. Vous devez lancer ce fichier via un terminal (terminal Linux ou VSCode selon votre préférence), nous utilisons Visual Studio Code et VS codium pour nos tests. <br/>
2 - Ouvrez votre navigateur web et entrez l'adresse localhost:5000 (Google Chorme, Mozilla Firefox, Microsoft EDGE et CCleaner Browser fonctionnent) <br/>
3 - Vous pouvez alors utiliser le site comme vous le souhaitez. <br/>
4 - Enfin, pour finir le processus, faites CTRL+C dans le terminal où vous avez lancé le serveur. <br/>

# Format des fichers .csv

Afin de garder les informations entre les différentes utilisations du serveur, nous utilisons des fichiers CSV. Vous trouverez deux types de fichier CSV :

## Le fichier csv contenant les utilisateurs

Ce fichier garde différentes informations sur les utilisateurs dans le format ci-dessous : <br/>
ID_User;NOM;EMAIL;hash du mot de passe

## Les fichiers csv contenant les questions des utilisateurs

Ces fichiers sont nommés en fonction de l'identifiant (ID_User) de l'utilisateur. Par exemple le fichier des questions de l'utilisateur 143 se nommera question_143.csv.<br/>
Ils respectent le format ci-dessous :<br/>
Id;ET1;ET2;ET3;...;FINET;Question;REP1;REP2;...;FINREP;BREP1;BREP2;...     (ET=étiquette REP=réponse BREP=Bonne réponse)<br/>

# Fonctionnalités

Toutes les fonctionnalités demandées sont présentes.

# Webographie

## Bibliothèques :
https://python-markdown.github.io/reference/<br/>
https://mermaid.js.org/#/<br/>
https://pypi.org/project/md-mermaid/<br/>
https://highlightjs.org/download/<br/>

## Documentation :
https://docs.python.org/3/<br/>
https://docs.python.org/fr/3/library/hashlib.html<br/>
https://pythonbasics.org/#Flask-Tutorial<br/>

# Attention
Le fichier mermaid.js et load-mathjax.js du dossier static et temp sont les codes sources des bibliothèques mermaid et mathjax. Nous les avons téléchargés séparément 
afin d'éviter de devoir installer entièrement la bibliothèque mermaid et mathjax. Ces fichiers ont été mis à la disposition de tous par les créateurs et n'ont pas été modifiés.
