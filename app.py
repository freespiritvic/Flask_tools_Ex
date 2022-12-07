from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def survey_start():
    """Homepage to survey."""
    return render_template('survey_start.html', survey=survey)


@app.route('/questions', methods=['POST'])
def questions():
    """Clear the responses."""
    session['responses'] = []
    return redirect('/questions/0')


@app.route('/answer', methods=['POST'])
def next_question():
    """Save response and onto the next question."""
    choice = request.form['answer']

    response = session['responses']
    response.append(choice)
    session['responses'] = response

    if (len(response) == len(survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f'/questions/{len(response)}')


@app.route('/questions/<int:que_id>')
def check_responses(que_id):
    """Display current question."""
    responses = session.get('responses')

    if (responses is None):
        return redirect("/")
    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    if (len(responses) != que_id):
        flash(f'Invalid question id: {que_id}.')
        return redirect(f'/questions/{len(responses)}')

    question = survey.questions[que_id]
    return render_template('questions.html', question_num=que_id, question=question)


@app.route('/complete')
def complete():
    """Show they completed the survey."""
    return render_template('complete.html')