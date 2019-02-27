# !/usr/bin/python

import os
import re
from tika import parser
from datetime import datetime
import time


def main():
    #rootdir = directory padre da cui verranno analizzati tutti i file delle subdirectories (considerare il percorso partendo dalla root della cartella Git)
    rootdir = 'doc'
    # foutdir = directory del file coi risultati (considerare il percorso partendo dalla root della cartella Git)
    foutdir = 'Gulpease/Risultati.txt'
    #extension = estensione dei file che si voglio analizzare. Insieme ad extension verranno annalizzati i file senza estensione
    extensions = '.pdf'

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            try:
                ext = os.path.splitext(file)[-1].lower()
                path = os.path.join(subdir, file)

                if ext in extensions:
                    #Vengono calcolati i dati per l'indice di Gulpease
                    testo = parser.from_file(path)['content']
                    parole = len(re.findall(r'\w+', testo))
                    lettere = len(re.findall(r'\w', testo))
                    punti = len(re.findall('[.]+\s', testo)) + (
                        len(re.findall('[;]+\s', testo)) - len(re.findall('[.]+\s+[.]', testo))
                    )

                    name = os.path.basename(path)
                    indiceG = (89+((300*punti)-(10*lettere))/parole)
                    indiceG = round(indiceG, 2)
                    #Viene creato o modificato il file nel path indicato
                    with open(foutdir, "a+") as fout:
                        fout.write(f"{name}: {indiceG}\t")
                    print(f"Parole: {parole} Lettere: {lettere} Punti: {punti}")
                    print(f"L'indice di {path} è: {indiceG}")
            except IOError:
                print("File doesn't exist")
    timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    with open(foutdir, "a+") as fout:
        fout.write(f"\t{timestamp}\n")


if __name__ == '__main__':
    main()
