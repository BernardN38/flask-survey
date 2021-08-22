from flask import Flask, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import  satisfaction_survey

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '<replace with a secret key>'
toolbar = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home():
    session['responses'] = []
    return render_template('home.html', survey=satisfaction_survey)

@app.route('/question/<num>')
def show_question(num):
    current = len(responses)
    if int(num) >= len(satisfaction_survey.questions)+1:
        return redirect('/thankyou')
    elif int(num) == current:
        return render_template('question.html', survey=satisfaction_survey, num=int(num), responses=responses, length=len(satisfaction_survey.questions), current_page = len(responses))
    else:
        flash('questions need to be answered in order')
        return redirect(f'/question/{current}')


@app.route('/answer', methods=['POST'])
def save_answer():
    responses_in_session = session['responses']
    responses_in_session.append(request.form.get('answer'))
    session['responses'] = responses_in_session
    responses.append(request.form.get('answer'))
    if len(responses) >= len(satisfaction_survey.questions):
        return redirect('/thankyou')
    else:
        return redirect(f'/question/{len(responses)+1}')

@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')

@app.route('/results')
def print_results():
    return render_template('results.html', responses=responses, survey=satisfaction_survey)