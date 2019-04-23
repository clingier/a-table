"""A-table: Skill Alexa."""
from flask import Flask, render_template
from flask_ask import Ask, question, session, statement

from api import (get_recette_par_etape, recherche_par_ingredients,
                 recherche_par_titre)
from utils import normalize_aliment_lists

app = Flask(__name__)
ask = Ask(app, '/')


@ask.launch
def atable_welcome():
    """Phrase de bienvenue qui presente l'application."""
    welcome = render_template('atable_ouverture')
    reprompt = render_template('atable_rappel')
    return question(welcome).reprompt(reprompt)


@ask.intent(
    'RechercheParTitre',
    mapping={'recette': 'recette'}
)
def exec_recherche_par_titre(recette):
    """Execute une recherche par titre et propose la recette a l'utilisateur.

    Arguments
    ---------

    recette: str
        titre de la recette a rechercher.
    """
    recettes = recherche_par_titre(recette)

    intro = render_template('atable_resultat_intro')

    # Sauvegarde de la recette dans la session
    session.attributes['dialog_context'] = 'prop_recette'
    session.attributes['recette'] = recettes[0]

    # Prend la premiere recette
    titre_recette = recettes[0]['title']
    return question(f"{intro}: {titre_recette}. Voulez vous lire la recette?")


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
    intro = render_template('atable_resultat_intro')

    # Sauvegarde de la recette dans la session
    session.attributes['dialog_context'] = 'prop_recette'
    session.attributes['recette'] = recettes[0]

    # Prend la premiere recette
    titre_recette = recettes[0]['title']
    return question(f"{intro}: {titre_recette}. Voulez vous lire la recette?")


@ask.intent('AMAZON.YesIntent')
def when_the_user_says_yes():
    """Quand l'utilisateur dit oui cette fonction est appellee.

    Il faut verifier qu'une recette a bien ete selectionnee et que
    l'utilisateur vient de la question "Voulez vous cuisinez maintenant?"
    Ensuite, la fonction recupere les etapes et les ingredients de la recette
    et propose a l'utilisateur de lire les ingredients.
    """
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
    """L'utilisateur a dit non, retourne le template de fermeture."""
    return statement(render_template('atable_fin'))


@ask.intent('AMAZON.NextIntent')
def prochaine_etape():
    """L'utilisateur demande la prochaine etape.

    1. On verifie que l'utilisateur est bien en train d'ecouter une recette
    2. On recupere la recette et l'index de l'etape activee.
    3. Si l'index depasse la taille des etapes il est arrive au bout.
    """
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
    """L'utilisateur demande l'etape precedente.

    1. On verifie qu'il est en train d'ecouter une recette.
    2. On recupere la recette.
    3. si il est au debut on lui signale qu'il est au debut.
    4. aussinon on renvoie l'etape.
    """
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
    """L'utilisateur demade de repeter l'etape.

    1. On verifie qu'il est en train d'ecouter une recette.
    2. on recupere la recette et l'etape
    3. Si l'index == -1 (au debut) ou si il est >= len(etapes) alors
    on renvoie un message d'aide.
    4. Aussinon on renvoie l'etape de la recette.
    """
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
    """Retourne un template d'aide."""
    return question(render_template('aide'))


def lecture_ingredients():
    """Lis une liste d'ingredients."""
    intro = render_template('lecture_ingredient_resultat')
    outro = render_template('lecture_ingredient_outro')
    ingredients = ", ".join(session.attributes['etape_recette']['ingredients'])
    return question(f"{intro} {ingredients}. {outro}")


@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
def nogo():
    """Fin de l'application ou l'utilisateur a dit 'stop'."""
    fin = render_template('atable_fin')
    return statement(fin)


if __name__ == "__main__":
    app.run()
