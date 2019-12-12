from flask import Blueprint, render_template, request, redirect, url_for, flash
from hktm import db
from hktm.models import Test
from hktm.tests.forms import AddForm

tests_bp = Blueprint('tests', __name__, template_folder='templates/tests')

## list route
@tests_bp.route('/list')
def list():
    tests = Test.query.all()
    return render_template('list_tests.html',tests=tests)



## add route
@tests_bp.route('/add',methods=['GET','POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        flash('New Test Created')
        name = form.name.data
        grade = form.grade.data
        comments = form.comments.data


        new_test = Test(name,grade,comments)
        db.session.add(new_test)
        db.session.commit()

        return redirect(url_for('test.edit'))

    return render_template('add_test.html',form=form)



### edit route, we need to provide a list of ALL questions as well as
#   those on this test.
@tests_bp.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    test_to_edit = Test.query.get(id)

    #TODO: get a list of all questions and questions on this test for organizing

    form = AddForm()

    if form.validate_on_submit():
        test_to_edit.name = form.name.data
        test_to_edit.grade = form.grade.data
        test_to_edit.comments = form.comments.data
        db.session.commit()
        return redirect(url_for('tests.list'))

    # pre-populate for form for editing
    elif request.method == 'GET':
        form.name.default = test_to_edit.name
        form.grade.default = test_to_edit.grade
        form.comments.default = test_to_edit.comments
        form.process()

    return render_template('edit_test.html',form=form)




    pass
