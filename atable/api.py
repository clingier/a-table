"""Fonctions qui interagissent avec marmitton."""
from typing import Dict, List
from urllib.parse import urlencode

import requests

from bs4 import BeautifulSoup


def api_requests(url: str) -> List[Dict[str, str]]:
    """Fait une requete au site de Marmiton.

    Arguments
    ---------
    url : string: url a envoyer a Marmiton.

    Return
    -------
    une liste de Dictionnaire, ou chaque dictionnaire est
    une recette.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    resultats_recherche = []
    liste_recette = soup.findAll('div', attrs={'class': 'recipe-card'})
    for recette in liste_recette:
        dict_recette = {}
        dict_recette['title'] = recette.find(
            'h4', attrs={'class': 'recipe-card__title'}).text
        dict_recette['url'] = recette.find(
            'a', attrs={'class': 'recipe-card-link'}).attrs['href']
        resultats_recherche.append(dict_recette)
    return resultats_recherche


def recherche_par_ingredients(ingredients: List[str]) -> List[Dict[str, str]]:
    """Recherche par ingredients et renvoie le resultat de la recherche.

    Arguments
    ---------
    Liste de string: chaque string represente un ingredient

    Return
    ------
    Liste de dictionnaire ou chaque dictionnaire represente une recette
    """
    url = 'https://www.marmiton.org/recettes/recherche.aspx?'
    encoded = urlencode({"aqt": "-".join(ingredients), "st": 1})
    results = api_requests(url + encoded)
    return results
