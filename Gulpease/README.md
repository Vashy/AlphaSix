# Avviare uno script in python quando avviene un trigger con Git

E' possibile crearlo in due modi:

1. Usando la libreria `python-githooks`
2. Scrivendo direttamente dentro gli **hook** di **.git/hooks**

## 1. Usando la libreria `python-githooks`

1. Scaricare la libreria `python-githooks` attraverso il comando
`pip install python-githooks`

2. Creare il file python che si vuole eseguire con l'evento di trigger

3. Creare nella root della cartella di Git il file *.githooks.ini* con all'interno scritto:
    ```bash
       # .githooks.ini

       [*nome_hook*]
       command = *comando_python*

       [*nome_hook*]
       command = *comando_python*
    ```
    In *nome_hook* inserire il nome di uno degli hook presenti in *.git/hooks* (senza il *.sample*) e in *comando_python* inserire il comando per eseguire il file creato al punto 2, considerando che la "posizione del terminale" si trova nella root della cartella Git.

    Un esempio:
    ```bash
        # .githooks.ini

        [pre-commit]
        command = python3 Gulpease/gulpeaseIndex.py
    ```

4. Eseguire, dalla root della cartella Git il comando `githooks` (da rieseguire ogni volta che si sposta il file creato nel punto 2). Questo comando crea un hook (nella cartella *.git/hooks*) del tipo indicato che esegue il file python creato

## Scrivendo direttamente dentro gli **hook** di **.git/hooks**

1. Creare nella cartella *.git/hooks* un file che indica il tipo di hook che si vuole usare (i nomi sono i titoli dei file già presenti) senza indicarne l'estensione

2. Scrivere lo script in python aggiungendo all'inizio del file `#!/usr/bin/env python`

# Script python gulpeaseIndex

1. Nella variabile `rootdir` indicare la directory padre da cui iniziare a cercare tutti i file (considerare il percorso partendo dalla root della cartella Git)
2. Nella variabile `extensions` indicare l'estensione del file che si vuole analizzare (considerare il percorso partendo dalla root della cartella Git)
3. Nella variabile `fout` indicare dove salvare i risultati