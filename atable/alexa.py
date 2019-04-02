from flask import Flask, render_template
from flask_ask import Ask, question, statement

app = Flask(__name__)
ask = Ask(app, '/')


@ask.intent('AtableWelcomeIntent')
def atable_welcome():
    welcome = render_template('atable_ouverture')
    reprompt = render_template('atable_rappel')
    return question(welcome).reprompt(reprompt)


@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
@ask.intent('AMAZON.NoIntent')
def trip_nogo():
    fin = render_template('atable_fin')
    return statement(fin)
