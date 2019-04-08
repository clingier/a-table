"""A-table: Skill Alexa."""

from flask import Flask, render_template
from flask_ask import Ask, context, delegate, question, session, statement

from api import get_recette_par_etape, recherche_par_ingredients
from utils import normalize_aliment_lists

app = Flask(__name__)
ask = Ask(app, '/')


@ask.launch
def atable_welcome():
    welcome = render_template('atable_ouverture')
    reprompt = render_template('atable_rappel')
    return question(welcome).reprompt(reprompt)


@ask.intent(
    'RechercheParIngredients',
    mapping={
        'aliments_phrase': 'aliments',
    })
def exec_recherche_par_ingredients(aliments_phrase):
    """Execute une recherche par ingredients et propose la recette a l'user.

    Arguments
    ---------
    aliments_phrase: str
        Bout de phrase recoltee par Alexa.

    Return
    ------
    out: question
        Question posee par Alexa qui propose la recette et demande si elle veut
        la cuisiner.

    Exemple
    -------
        exec_recherche_par_ingredients(
            "de la mozarella, du melon et du jambon"
            )

        output: question(
            "Voici la recette que j'ai trouve: {salade de melon mediteraneene}
            Voulez vous la cuisiner maintenant?
            "
            )
    """
    # Recuperer la liste d'arguments
    aliments = normalize_aliment_lists(aliments_phrase)
    # Demander les recettes a marmiton
    recettes = recherche_par_ingredients(aliments)
    # Phrase d'intro detaillee dans templates.yaml
    intro = render_template('atable_resultat')

    # Sauvegarde de la recette dans la session
    session.attributes['dialog_context'] = 'prop_recette'
    session.attributes['recette'] = recettes[0]

    # Prend la premiere recette
    titre_recette = recettes[0]['title']
    return question(f"{intro}: {titre_recette}. Voulez vous lire la recette?")


@ask.intent('AMAZON.YesIntent')
def when_the_user_says_yes():
    # Est ce que l'utilisateur vient de la question 'Voulez vous cuisiner mnt?'
    want_to_cook = session.attributes.get('dialog_context') == 'prop_recette'
    # On s'assure que l'utilisateur a deja trouve une recette
    valid_recette = session.attributes.get('recette') is not None

    if want_to_cook and valid_recette:
        # Recupere la recette
        recette = session.attributes['recette']
        # Demande les etapes a Marmitton
        etape_recette = get_recette_par_etape(recette['url'])
        # Sauvegarde les etapes de la recette
        session.attributes['etape_recette'] = etape_recette

        # Contexte de lecture de recette
        session.attributes['dialog_context'] = 'lecture_recette'

        session.attributes['index_etape'] = -1

        return lecture_ingredients()


@ask.intent('AMAZON.NoIntent')
def non():
    return statement(render_template('atable_fin'))


@ask.intent('AMAZON.NextIntent')
def prochaine_etape():

    if session.attributes.get('dialog_context') != 'lecture_recette':
        return aide_usage()

    etape_recette = session.attributes['etape_recette']['etapes']

    index = session.attributes['index_etape']
    response = ""
    if index == -1:
        response += render_template('lecture_de_recette_intro')

    index += 1

    if index >= len(etape_recette):
        response = render_template('lecture_de_recette_fin')
    else:
        etape = etape_recette[index]
        response += " " + etape

    session.attributes['index_etape'] = index
    return question(response)


@ask.intent('AMAZON.PreviousIntent')
def etape_precedente():
    if session.attributes.get('dialog_context') != 'lecture_recette':
        return aide_usage()

    etape_recette = session.attributes['etape_recette']['etapes']
    index = session.attributes['index_etape']
    response = ""

    if index == 0 or index == -1:
        response = render_template('etape_precedente_erreur')
        return question(response)

    index -= 1
    etape = etape_recette[index]
    session.attributes['index_etape'] = index
    return question(etape)


@ask.intent('AMAZON.RepeatIntent')
def repete_etape():
    if session.attributes.get('dialog_context') != 'lecture_recette':
        return aide_usage()

    etape_recette = session.attributes['etape_recette']['etapes']
    index = session.attributes['index_etape']

    if index == -1 or index >= len(etape_recette):
        return question("Vous etes arrive au bout de la recette ou vous",
                        " n'avez pas encore commence")

    etape = question(etape_recette[index])
    return etape


def aide_usage():
    return question(render_template('aide'))


def lecture_ingredients():
    intro = render_template('lecture_ingredient_resultat')
    outro = render_template('lecture_ingredient_outro')
    ingredients = ", ".join(session.attributes['etape_recette']['ingredients'])
    return question(f"{intro} {ingredients}. {outro}")


@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
@ask.intent('AMAZON.NoIntent')
def nogo():
    fin = render_template('atable_fin')
    return statement(fin)


if __name__ == "__main__":
    app.run()
