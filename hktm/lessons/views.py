from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required,current_user
from hktm import db
from hktm.models import Lesson, LessonMaterial, MaterialType
from hktm.lessons.forms import AddForm, MaterialForm
from hktm.lesson_contents.RenderContent_KJTS import RenderContentKJTS
from flask_babel import _

lessons_bp = Blueprint('lessons', __name__, template_folder='templates/lessons')
## list route
@lessons_bp.route('/list')
@login_required
def list():
    #get a list of the active users grades for the grade drop down
    grades = current_user.grades.replace('A','')

    #get a list of all lessons - the template will tabetise them
    lessons = db.session.query(Lesson).filter(Lesson.grade.in_(current_user.grades)).order_by(Lesson.name)
    #assert 0
    return render_template('list_lessons.html',lessons=lessons, grades=grades)



## add route
@lessons_bp.route('/add',methods=['GET','POST'])
@login_required
def add():
    form = AddForm()

    #get a list of the active users grades for the grade drop down
    grades = current_user.grades.replace('A','')
    form.grade.choices = [(g, g) for g in grades]

    if form.validate_on_submit():
        print('valid')
        flash('New Lesson Created')
        name = form.name.data
        grade = form.grade.data

        new_lesson = Lesson(name, grade)
        db.session.add(new_lesson)
        db.session.commit()
        print ('processing')
        return redirect(url_for('lessons.edit',id=new_lesson.id))

    print('no validation')
    return render_template('add_lesson.html',form=form)


@lessons_bp.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    lesson_to_delete = Lesson.query.get(id)

    lesson_name = lesson_to_delete.name
    flash(f'Lesson {lesson_name} deleted.')
    db.session.delete(lesson_to_delete)
    db.session.commit()
    return redirect(url_for('lessons.list'))


### edit route, we need to provide a list of ALL questions as well as
#   those on this test.
@lessons_bp.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit(id):
    lesson_to_edit = Lesson.query.get(id)

    form = AddForm()

    #get a list of the active users grades for the grade drop down
    grades = current_user.grades.replace('A','')
    form.grade.choices = [(g, g) for g in grades]

    form.grade.default = lesson_to_edit.grade
    content_list = MaterialType.query.all()
    lesson_content = LessonMaterial.query.filter_by(lesson_id=id)
    form.name.default = lesson_to_edit.name
    form.process()

    if form.validate_on_submit():
        lesson_to_edit.name = form.name.data
        # lesson_to_edit.date = form.date.data
        lesson_to_edit.grade = form.grade.data
        # lesson_to_edit.comments = form.comments.data
        db.session.commit()
        return redirect(url_for('lessons.list'))
    return render_template('edit_lesson.html',form=form,
                            lesson_id=lesson_to_edit.id,
                            lesson_content = lesson_content,
                            content_types=content_list
                            )


@lessons_bp.route('/kanji_test_preview/<string:content>', methods=['GET','POST'])
@login_required
def kanji_test_preview(content):
    mat = RenderContentKJTS(content)
    return render_template('kanji_test_preview.html',test=mat);


@lessons_bp.route('/kanji_test_print/<string:content>', methods=['GET','POST'])
@login_required
def kanji_test_pint(content):
    mat = RenderContentKJTS(content)
    return render_template('kanji_test_print.html',test=mat);
