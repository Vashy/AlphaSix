"""
Per usare, basta eseguire python3 glossarizzatore.py
Il controllo viene effettuato solo sui file necessari

TODO
Manca l'albero di struttura in json per controllo
"""
import fileinput
from pathlib import Path
import re

re_label = re.compile(r'\\label{[a-zA-Z][^}]+}')
re_glossary = re.compile(r'\\gloss{[^}]*}')
re_word_escaper = re.compile(r'[\.?!;:,()]')
glossarydir = Path('./Esterni/Glossario/sections')
glossario=[]
localdir = Path('.')

#Rimuovo i \gloss presenti
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
            checks = re_glossary.findall(line)
            for check in checks:
                match = check.replace('\gloss{','')
                match = match.replace('}','')
                line = line.replace(check,match)
            print(line, end='')

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
        
glossario_copy = glossario[:]

#Cerco nei documenti le parole
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
        for line in fileinput.input(str(i), inplace = True):
            words = line.split();
            for i,word in enumerate(words):
                word_escaped = re_word_escaper.sub(' ', word)
                word_escaped = word_escaped.replace(' ','')
                words[i] = word_escaped
            #TODO
            #Controllare di aver cambiato documento, non file
            if fileinput.isfirstline():
                glossario = glossario_copy[:]
            for parola in glossario:
                parola_escaped = parola.replace(' ','')
                if parola_escaped in words and line[0]!='%':
                    line = line.replace(parola,'\gloss{'+parola+'}', 1)
                    if parola in glossario: glossario.remove(parola)
                    if parola.lower() in glossario: glossario.remove(parola.lower())
                    if parola.upper() in glossario: glossario.remove(parola.upper())
                    if parola.capitalize() in glossario: glossario.remove(parola.capitalize())
                    if parola.title() in glossario: glossario.remove(parola.title())

            print(line, end='')