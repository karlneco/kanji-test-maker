from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretsquirrel'

class QuestionForm(FlaskForm):
    question_type = SelectField(u'What type of question is this', choices=[(1,'Reading'),(2,'Writing'),(3,'Combination')])
    question_text = StringField('Enter the question using the appropriate syntax:')
    submit = SubmitField('Save Question')

@app.route('/')
def index():
    question_count = 100
    test_count = 4
    return render_template('index.html', question_count=question_count,test_count=test_count)

@app.route('/questions')
def questions():
    return render_template('questions.html')

@app.route('/new_question',methods=['GET','POST'])
def new_question():
    question_text = False

    form = QuestionForm()
    if form.validate_on_submit():
        question_text = form.question_text.data
        question_type = form.question_type.data
    return render_template('new_question.html',form=form, questions_text=question_text)

@app.route('/tests')
def tests():
    return render_template('tests.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
