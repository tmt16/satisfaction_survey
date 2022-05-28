from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

RESPONSES = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def start_page():
    """Select a survey."""
    return render_template("start_page.html", satisfaction_survey=satisfaction_survey)

@app.route("/start", methods=["POST", "GET"])
def start():
    """Clear response session"""
    session[RESPONSES] = []
    return redirect("/questions/0")

@app.route("/questions/<int:id>")
def questions(id):
    """Display questions and radio button choices on each page"""

    responses_session = session.get(RESPONSES)

    # If user has not answered any questions, redirect to route
    if (responses_session is None):
        return redirect("/")        
    
    # If user has answered all questions, redirect to thank you page.    
    if (len(responses_session) == len(satisfaction_survey.questions)):
        return redirect("/thank_you")

    # If user tries to access a question out of order, redirect to current question.
    if (len(responses_session) != id):
        flash(f"Question {id + 1} has already been completed.")
        return redirect(f"/questions/{len(responses_session)}")

    return render_template("questions.html", satisfaction_survey=satisfaction_survey.questions[id], id=id)

@app.route("/answer/<int:id>", methods=["POST"])
def answer(id):
    """Append answers to RESPONSES"""

    answer = request.form["answer"]
    question_answers = session[RESPONSES]
    question_answers.append(answer)
    session[RESPONSES] = question_answers
    next_question = id + 1

    # if user has reached the end of the survey, go to thank you page
    if (len(question_answers) == len(satisfaction_survey.questions)):
        return redirect("/thank_you")
    else:
        return redirect("/questions/" + str(next_question))

@app.route("/thank_you")
def thank_you():
    """Thank you/completion page."""
    return render_template("thank_you.html")


 
