from flask import Blueprint, render_template, request, redirect, url_for, flash
from hktm import db
from hktm.questions.core import question_factory
from hktm.models import Question
from hktm.questions.forms import AddForm

questions_bp = Blueprint('questions', __name__, template_folder='templates/questions')


## list route for questions
@questions_bp.route('/list')
def list():
    questions = Question.query.all()
    return render_template('list_questions.html',questions=questions)


## add route
@questions_bp.route('/add', methods=['GET','POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        flash('New Question Created')
        type = form.type.data
        grade = form.grade.data
        question = form.question.data

        new_question = Question(type,grade,question)
        db.session.add(new_question)
        db.session.commit()

        return redirect(url_for('questions.list'))

    return render_template('add_question.html',form=form)


### edit route, also creates the preview of the question using the appropriate
#   question object
@questions_bp.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    question_to_edit = Question.query.get(id)

    # use the factory to create the appropriate object type
    question_object = question_factory(question_to_edit)

    form = AddForm()
    if form.validate_on_submit():
        flash('New Question Created')
        question_to_edit.type = form.type.data
        question_to_edit.grade = form.grade.data
        question_to_edit.question = form.question.data
        db.session.commit()
        return redirect(url_for('questions.list'))

    # pre-populate for form for editing
    elif request.method == 'GET':
        form.type.default = question_to_edit.type
        form.grade.default = question_to_edit.grade
        form.question.default = question_to_edit.question
        form.process()

    return render_template('edit_question.html',form=form,question=question_object)
