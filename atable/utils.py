"""Des fonctions utiles pour notre skill Alexa."""
import os
from typing import List

import pandas as pd

from unidecode import unidecode

from . import ROOT_DIR


def normalize_aliment_lists(string: str) -> List[str]:
    """Trouve les aliments citee dans une phrase et renvoie une liste.

    Unidecode est utilise pour normaliser les phrase afin de retirer les
    accents des mots. Tout les mots sont mis en minuscule aussi.

    Args
    ----
    string: La phrase qui contient plein de mots, dont certains sont des
    aliments

    Return
    ------
    Une liste de noms d'aliments
    """
    # La liste d'aliments (vide pour le moment)
    liste_aliments = []

    # Recupere la base de donnee
    df = pd.read_csv(os.path.join(ROOT_DIR, 'ingredients.csv'))

    # NORMALISATION:
    # Enleve les accents et les caractere non-ascii
    string = unidecode(string)
    # Mets toute la phrase en minuscule
    string = string.lower()

    for word in string.split():
        # Pour chaque mots
        if word in df.ingredients.values:
            # si le mot est dans notre base de donnee, on l'ajoute.
            liste_aliments.append(word)

    return liste_aliments
