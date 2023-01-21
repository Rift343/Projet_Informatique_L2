#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 09:59:30 2023

@author: clement.chevalier01@etu.umontpellier.fr
"""

import markdown
import md_mermaid



def BufferToHtml(text,typeBuff):
    """
    Prends en entré du text et le type de text à traduire en html
    et retourne les balises html sous forme d'une string
    """
    if typeBuff == "mermaid": #si le type du text envoyé est mermaid on le place entre des balise pre avec comme class mermaid ce qui permet à la bibliothèque mermaid de le reconnaître comme un graph et de l'afficher comme il se doit
        return "<br><pre class='mermaid'>"+text+"</pre><br>"
    elif typeBuff == "latex": #si le type du text envoyé est latex alors on le place entre des dollars afin que que la bibliothèque mathjax puisse l'interpréter comme du latex
        return "<br>$"+text+"$<br><br>"
    else: #dans tous les autres cas le type du text envoyé est du code donc on entoure le text de balise code pour que la bibliothèque highlight puisse coloré le code
        return "<br><pre><code class="+typeBuff+" style='background-color:white'>"+text+"</code></pre><br>"



def markdownToHtml(text):
    """
    Prends une string contenant du markdown comprenant des graphes, du code et du latex.
    Retourne une string avec tous le code traduit en html
    """
    html = "" #sert à contenir la traduction du text en html
    textBuffer = ""
    typePar = [1,""]
    markdownText = text.split("\n") #on split le text sur les retours à la ligne pour travailler ligne par ligne
    for line in markdownText:
        if line[0:3] == "```":
            if line[3:] != "": #si une ligne commence par ``` et un autre mot alors on stoque ce mot qui est le type de la portion de text dans typePar
                typePar[1] = line[3:]
                textBuffer = ""
            else: #si la ligne commence par ``` uniquement alors c'est que textBuffer est rempli de text du type contenu dans typePar
                html += BufferToHtml(textBuffer,typePar[1].split("\n")[0]) #On ajoute donc à html le rendu en html de ce text afin qu'il puisse être bien affiché
            typePar[0] = typePar[0]*-1 #quoi qu'il arrive si la ligne a commencé par ``` on change de type de paragrahe
        elif typePar[0] == -1:
            textBuffer += line+"\n" #typePar[0] == -1 signifie que la ligne lu n'est pas écrite en markdown
        else:
            html += markdown.markdown(line) #on utilise la bibliothéque markdown afin de traduire la ligne écrite en markdown en html
    return html


def liMarkdownToHtml(li):
    """
    prend en entré une liste et traduit tous les élément de li en html
    et retourne cette même liste modifié
    """
    for i in range(len(li)):
        li[i]= markdownToHtml(li[i]);
    return li;
