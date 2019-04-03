"""Fonctions qui interagissent avec marmitton."""
from typing import Dict, List
from urllib.parse import urlencode

import requests

from bs4 import BeautifulSoup


def api_request(url: str) -> List[Dict[str, str]]:
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
    results = api_request(url + encoded)
    return results


def get_recette_par_etape(recipe_url: str) -> Dict[str, List[str]]:
    """Obtient la structure d'une recette, cad les etapes et les ingredients.

    Arguments
    ---------
    recipe_url: adresse vers la recette a scraper.

    Return
    ------
    Un dictionnaire de cette forme dict_ = {'ingredients': [..], 'etapes':[..]}
    Exemple:
    oeuf_a_la_coque = {
        'ingredients': ['oeuf'],
        'etapes' : ['faire bouillir de l'eau', 'plonger l'oeuf', ..]
    }
    """
    marmiton_url = 'https://www.marmiton.org'
    response = requests.get(marmiton_url + recipe_url)
    soup = BeautifulSoup(response.text)
    ingredients = soup.select('.recipe-ingredients__list__item')
    ingredients = [re.sub(r'\s+', ' ', ing.text.strip())
                   for ing in ingredients]
