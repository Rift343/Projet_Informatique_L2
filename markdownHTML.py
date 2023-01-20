#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 09:59:30 2023

@author: clement.chevalier01@etu.umontpellier.fr
"""

import markdown
import md_mermaid


import markdown
import md_mermaid


def BufferToHtml(text,typeBuff):
    if typeBuff == "mermaid":
        return "<br><pre class='mermaid'>"+text+"</pre><br>"
    elif typeBuff == "latex":
        return "<br>$"+text+"$<br><br>"
    else:
        return "<br><pre><code class="+typeBuff+" style='background-color:white'>"+text+"</code></pre><br>"



def markdownToHtml(text):
    """
    Prends une string contenant du markdown comprenant des graphes, du code et du latex.
    Retourne une string avec tous le code traduit en html
    """
    html = ""
    textBuffer = ""
    typePar = [1,""]
    markdownText = text.split("\n")
    for line in markdownText:
        if line[0:3] == "```":
            if line[3:] != "":
                typePar[1] = line[3:]
                textBuffer = ""
            else:
                html += BufferToHtml(textBuffer,typePar[1].split("\n")[0])
            typePar[0] = typePar[0]*-1
        elif typePar[0] == -1:
            textBuffer += line+"\n"
        else:
            html += markdown.markdown(line)
    return html


def liMarkdownToHtml(li):
    for i in range(len(li)):
        li[i]= markdownToHtml(li[i]);
    return li;