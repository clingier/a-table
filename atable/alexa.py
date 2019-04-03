"""A-table: Skill Alexa"""
import datetime
import logging

from api import recherche_par_ingredients
from flask import Flask, render_template
from flask_ask import Ask, context, delegate, question, session, statement
from utils import normalize_aliment_lists

app = Flask(__name__)
ask = Ask(app, '/')


@ask.on_session_started
def start_session():
    logging.debug("Session Started at {}".format(datetime.now().isoformat()))


@ask.launch
def atable_welcome():
    session.attributes['dialog_context'] = 'LAUNCH'
    welcome = render_template('atable_ouverture')
    reprompt = render_template('atable_rappel')
    return question(welcome).reprompt(reprompt)


@ask.intent(
    'RechercheParIngredients',
    mapping={
        'aliments_phrase': 'aliments',
    })
def exec_recherche_par_ingredients(aliments_phrase):
    aliments = normalize_aliment_lists(aliments_phrase)
    recettes = recherche_par_ingredients(aliments)
    intro = render_template('atable_resultat')
    titres_recettes = [recette['title'] for recette in recettes][:3]
    reponse_alexa = ", ".join(titres_recettes)
    return statement(f"{intro}: {reponse_alexa}")


@ask.intent('AMAZON.YesIntent')
def response():
    if session.attributes['dialog_context'] == 'LAUNCH':
        statement(render_template('atable_demarrage'))
        session.attributes['dialog_context'] = 'SEARCH_CHOICE'
        choix_recherche = render_template('atable_choix_recherche')
        return question(choix_recherche)
    if session.attributes['dialog_context'] == 'SEARCH_CHOICE':
        return question("Quels ingredients avez vous sous la main?")


@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
@ask.intent('AMAZON.NoIntent')
def nogo():
    fin = render_template('atable_fin')
    return statement(fin)


if __name__ == "__main__":
    app.run()
