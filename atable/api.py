"""Fonctions qui interagissent avec marmitton."""
import re
from typing import Dict, List
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

MARMITTON_URL = 'https://www.marmiton.org/recettes/recherche.aspx?'

__all__ = ["api_request", "recherche_par_ingredients", "recherche_par_titre"]


def api_request(url: str) -> List[Dict[str, str]]:
    """Scrape les titres et liens des resultats de la recherche Marmitton.

    Cette fonction est utile a la fois pour la recherche par ingredient et
    pour la recherche classique.

    Arguments
    ---------
    url : string
        Url a envoyer a Marmiton.

    Return
    -------
    out: List[Dict[str, str]]
        Liste de Dictionnaire, ou chaque dictionnaire est une recette.
        format:
            {'title': 'Spaghetti Bolognaise', 'url': 'url_vers_la_recette'}
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


def recherche_par_titre(titre: str) -> List[Dict[str, str]]:
    """Cherche le titre de la recette sur Marmitton.

    Arguments
    ---------
    titre: str
        Nom de la recette a chercher.

    Return
    ------
    out: List[Dict[str, str]]
        Liste de dictionnaire ou chaque dictionnaire represente une recette.
        format:
            voir api_request()
    """
    encoded = urlencode({"aqt": titre, "st": 0})
    results = api_request(MARMITTON_URL + encoded)
    return results


def recherche_par_ingredients(ingredients: List[str]) -> List[Dict[str, str]]:
    """Encode les ingredients dans un url renvoie le resultat de la recherche.

    Cette fonction utilise api_request().

    Arguments
    ---------
    ingredients: List[str]
        Liste de string ou chaque string represente un ingredient

    Return
    ------
    out: List[Dict[str,str]]
        Liste de dictionnaire ou chaque dictionnaire represente une recette

    Exemple
    -------
        $ recherche_par_ingredients(['tomate', 'basilic', 'carotte'])
            [
                {'title': 'Bolognaise', 'url': 'http://...'},
                {'title': 'Lasagne', 'url': 'http://...'}
            ]
    """
    encoded = urlencode({"aqt": "-".join(ingredients), "st": 1})
    results = api_request(MARMITTON_URL + encoded)
    return results


def get_recette_par_etape(recipe_url: str) -> Dict[str, List[str]]:
    """Obtient la structure d'une recette, cad les etapes et les ingredients.

    Arguments
    ---------
    recipe_url: str
        Adresse vers la recette a scraper.

    Return
    ------
    recipe_dict: Dict[str, List[str]]
        Un dictionnaire de cette forme:
        recipe_dict = {
            'ingredients': [..],
            'etapes':[..]
        }

    Exemple:
    --------

        oeuf_a_la_coque = {
        'ingredients': ['oeuf'],
        'etapes' : ['faire bouillir de l'eau', 'plonger l'oeuf', ..]
        }
    """
    marmiton_url = 'https://www.marmiton.org'

    # Requete a marmitton
    response = requests.get(marmiton_url + recipe_url)

    # Initialisation de bs4 pour scraper
    soup = BeautifulSoup(response.text)

    # Scrap des ingredients
    ingredients = soup.select('.recipe-ingredients__list__item')

    # Scrap des etapes
    etapes = soup.select(".recipe-preparation__list__item")

    # Supp. des espaces par exemple 'debut\n\n\n\n\n\n suite'->'debut suite'
    etapes = [re.sub(r'\s+', ' ', etape.text.strip()) for etape in etapes]
    ingredients = [re.sub(r'\s+', ' ', ing.text.strip())
                   for ing in ingredients]

    recipe_dict = {
        'ingredients': ingredients,
        'etapes': etapes
    }

    return recipe_dict
