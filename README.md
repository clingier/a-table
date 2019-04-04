# A table!

A table est un skill Alexa. Decouvrez toute les recettes Marmiton par la voix.

## Voice User Interface

1) L'utilisateur declenche l'application: par son nom, ou en disant 'Cherche une recette avec A table'

**Premiere requete**
2) Choix, soit recherche par le nom soit par les ingredients.

### Si par le nom

3) Alexa prend le premier resultats de la recherche et dis son nom, 'J'ai trouve {nom de la recette}'


### Si par les ingredients

**Requete** Trois ingredients.

3) L'utilisateur enumere les ingredients

4) Alexa repete ce qu'elle a entendu comme ingredients. 

6) faire la recherche

7) Une fois la recherche terminee, elle propose les trois premiers titres

8) L'utilisateur choisi une des recettes.

**Requete** choix entre 3 recettes 1, 2 ou 3

### Lecture de la recette

Alexa separe bien toutes les etapes de la recette, l'utilisateur.

Il dit a alexa quand passer a l'etape suivante.

Et peut demander de repeter si il le faut.

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