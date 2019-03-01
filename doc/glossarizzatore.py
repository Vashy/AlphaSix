"""
Per usare, basta eseguire python3 glossarizzatore.py
Il controllo viene effettuato solo sui file necessari

TODO
Rimozione dei gloss presenti
Controllo inclusione dei file (altrimenti non serve a un granche')
"""


import fileinput
from pathlib import Path
import re
import os

re_label = re.compile(r'\\label{[a-zA-Z][a-zA-Z\s]+}')
re_alfa = re.compile(r'[,\.!?()]')
glossarydir = Path('./Esterni/Glossario/sections')
glossario=[]

#Cerco nel glossario le parole
for file in glossarydir.glob('**/*.tex'):
    for line in fileinput.input(str(file)):
        check = re_label.search(line)
        if check:
            match = check.group(0)
            match = match.replace('\label{','')
            match = match.replace('}','')
            glossario.append(match)
            glossario.append(match.lower())
            glossario.append(match.upper())
            glossario.append(match.capitalize())
            glossario.append(match.title())
        
glossario_copy = glossario

#Cerco nei documenti le parole
localdir = Path('.')
for i in localdir.glob('**/*.tex'):
    #In alcuni posti non cerco
    if ('template' not in str(i)
        and 'Glossario' not in str(i)
        and 'diario' not in str(i)
        and ('sections' in str(i)
             or 'descrizione' in str(i)
             or 'Verbali' in str(i)
             )
        ):
        for line in fileinput.input(str(i), inplace=True):
            
            #TODO
            #Controllare di aver cambiato documento, non file
            
            if fileinput.isfirstline():
                glossario = glossario_copy
            for parola in glossario:
                found = False
                if(not(' ' in parola)):
                    words = line.split()
                    for i,word in enumerate(words):
                        word = re_alfa.sub('',word)
                        if parola == word:
                            word = word.replace(parola,'\gloss{'+parola+'}')
                            words[i] = word
                            found = True
                    words = ' '.join(words)
                else:
                    words = line.split()
                    words = ' '.join(words)
                    count = 0
                    words = words.replace(parola,'\gloss{'+parola+'}',count)
                    if count > 0:
                        found = True
                        
                #Preservo l'indentazione
                spaces=''
                for i in range(0,len(line)):
                    if(line[i]==' ' or line[i]=='\t'):
                        spaces += line[i]
                    else:
                        break
                line = spaces+words
                
                
                #Rimuovo le parole trovate
                if found:
                    if parola in glossario: glossario.remove(parola)
                    if parola.lower() in glossario: glossario.remove(parola.lower())
                    if parola.upper() in glossario: glossario.remove(parola.upper())
                    if parola.capitalize() in glossario: glossario.remove(parola.capitalize())
                    if parola.title() in glossario: glossario.remove(parola.title())
            #Scrivo nel documento
            print(line)