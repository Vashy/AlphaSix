"""
Per usare, basta eseguire python3 glossarizzatore.py
Il controllo viene effettuato solo sui file necessari
"""

import fileinput
from pathlib import Path
import re
import itertools

re_label = re.compile(r'\\label{[a-zA-Z][^}]+}')
re_glossary = re.compile(r'\\gloss{[^}]*}')
glossarydir = Path('./Esterni/Glossario/sections')
glossario=[]
localdir = Path('.')

#Cerco nel glossario le parole
for file in glossarydir.glob('**/*.tex'):
    for line in fileinput.input(str(file)):
        check = re_label.search(line)
        if check:
            match = check.group(0)
            match = match.replace('\label{','')
            match = match.replace('}','')
            words = match.split()
            possibilities = []
            for word in words:
                possibility = []
                possibility.append(word)
                possibility.append(word.lower())
                possibility.append(word.upper())
                possibility.append(word.capitalize())
                possibilities.append(possibility)
            all_possibilities = list(itertools.product(*possibilities))
            for i,possibility in enumerate(all_possibilities):
                all_possibilities[i] = ' '.join(possibility)           
            glossario += all_possibilities
        
glossario_copy = glossario[:]

snippets = [
    "snippets/riferimenti_esterni.tex",
    "snippets/scopo_prodotto.tex"
]

ndp = [
    "Interni/Norme di Progetto/sections/introduzione.tex",
    "Interni/Norme di Progetto/sections/processi_primari.tex",
    "Interni/Norme di Progetto/sections/processi_organizzativi.tex",
    "Interni/Norme di Progetto/sections/processi_di_supporto.tex"
]

adr = [
    "Esterni/Analisi dei Requisiti/sections/introduzione.tex",
    "Esterni/Analisi dei Requisiti/sections/descrizione_generale.tex",
    "Esterni/Analisi dei Requisiti/sections/use_cases.tex",
    "Esterni/Analisi dei Requisiti/sections/requisiti.tex",
    "Esterni/Analisi dei Requisiti/sections/appendice_A.tex"
]

pdp = [
    "Esterni/Piano di Progetto/sections/introduzione.tex",
    "Esterni/Piano di Progetto/sections/analisi_dei_rischi.tex",
    "Esterni/Piano di Progetto/sections/pianificazione.tex",
    "Esterni/Piano di Progetto/sections/suddivisione_del_lavoro.tex",
    "Esterni/Piano di Progetto/sections/prospetto_economico.tex",
    "Esterni/Piano di Progetto/sections/preventivo.tex",
    "Esterni/Piano di Progetto/sections/organigramma.tex",
    "Esterni/Piano di Progetto/sections/consuntivo.tex",
    "Esterni/Piano di Progetto/sections/attualizzazione_rischi.tex"
]

pdq = [
    "Esterni/Piano di Qualifica/sections/introduzione.tex",
    "Esterni/Piano di Qualifica/sections/qualita_processo.tex",
    "Esterni/Piano di Qualifica/sections/qualita_prodotto.tex",
    "Esterni/Piano di Qualifica/sections/test.tex",
    "Esterni/Piano di Qualifica/sections/standard_qualita.tex",    
    "Esterni/Piano di Qualifica/sections/resoconto_attivita_verifica.tex",    
    "Esterni/Piano di Qualifica/sections/mitigazione_variazioni.tex",    
    "Esterni/Piano di Qualifica/sections/valutazioni.tex"
]

#Array con i documenti da glossarizzare
documents = [pdp]

#Rimuovo i \gloss presenti
for document in documents:
    for line in fileinput.input(document, inplace=True):
        checks = re_glossary.findall(line)
        for check in checks:
            match = check.replace('\gloss{','')
            match = match.replace('}','')
            line = line.replace(check,match)
        print(line, end='')


#Cerco nei documenti le parole
for document in documents:
    for numfile,file in enumerate(document):
        if numfile == 0:
            glossario = glossario_copy[:]
        for line in fileinput.input(file, inplace=True):
            for parola in glossario:
                re_word_escaper = re.compile(r'\b'+re.escape(parola)+r'\b')
                if (re.search(re_word_escaper, line)):
                    word = re.search(re_word_escaper, line).group()
                    if parola == word and line[0]!='%':
                        line = line.replace(parola,'\gloss{'+parola+'}', 1)
                        if parola in glossario: glossario.remove(parola)
            print(line, end='')