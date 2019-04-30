# A table!

A table est un skill Alexa. Decouvrez toute les recettes Marmiton par la voix.

## Voice User Interface

L'utilisateur declenche l'application: par son nom, ou en disant 'Cherche une recette avec A table'

### Recherche par ingredients:

- "Qu'est ce que je peux cuisiner/faire avec {phrase contenant les ingredients}"
- "Cherche/Recherche par ingredients {phrase contenant les ingredients}"
- "Cherche une recette par ingredients {phrase contenant les ingredients}"

### Recherche par titre:

- "Comment cuisiner/faire un {titre}"
- "Je voudrais cuisiner {titre}"
- "Recherche par titre {titre}"

### Lecture de recette:

- passer a l'etape suivante: "prochaine etape", "etape suivante"
- revenir a l'etape precedente: "etape precedente"
- repeter l'etape: "repete"

### Demande d'aide:

- "Qu'est ce que je peux faire"
- "A l'aide"

# Tutoriel Installation

1. Clonez ce repo avec `git clone https://github.com/clingier/a-table.git`.
2. Installez [Miniconda avec Python 3](https://conda.io/miniconda.html).
   Si vous avez deja `conda` installe, vous pouvez executez `conda update -n base conda`.
3. Executez `conda env create -f environment.yml` a partir de la ou vous avez clone le repo
4. Activez l'environnement en executant
    pour mac:
        `source activate open-for-business-local-env`
    pour windows:
        `set PATH=C:\Anaconda\envs\a-table\Scripts;C:\Anaconda\envs\a-table;%PATH%`
        `activate a-table` -> pas sur que ca fonctionne

    Si vous avez des erreurs essayez -> `conda activate a-table`
