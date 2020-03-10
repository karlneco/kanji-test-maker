from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required,current_user
from hktm import db
from hktm.models import Lesson, LessonMaterial, MaterialType
from hktm.lessons.forms import AddForm, MaterialForm
from flask_babel import _

lessons_bp = Blueprint('lessons', __name__, template_folder='templates/lessons')
## list route
@lessons_bp.route('/list')
@lessons_bp.route('/list/<int:jump>', methods=['GET'])
@login_required
def list(jump=0):
    #get a list of the active users grades for the grade drop down
    grades = current_user.grades.replace('A','')

    #get a list of all lessons - the template will tabetise them
    lessons = db.session.query(Lesson).filter(Lesson.grade.in_(current_user.grades)).order_by(Lesson.name)
    #assert 0
    return render_template('list_lessons.html',lessons=lessons, grades=grades, jump=jump)



## add route
@lessons_bp.route('/add',methods=['GET','POST'])
@login_required
def add():
    form = AddForm()

    #get a list of the active users grades for the grade drop down
    grades = current_user.grades.replace('A','')
    form.grade.choices = [(g, g) for g in grades]

    if form.validate_on_submit():
        flash(_('New Lesson Created'))
        name = form.name.data
        grade = form.grade.data

        new_lesson = Lesson(name, grade)
        db.session.add(new_lesson)
        db.session.commit()
        return redirect(url_for('lessons.edit',id=new_lesson.id))

    return render_template('add_lesson.html',form=form)


@lessons_bp.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    lesson_to_delete = Lesson.query.get(id)

    for m in lesson_to_delete.lesson_materials:
        db.session.delete(m)

    lesson_name = lesson_to_delete.name
    grade = lesson_to_delete.grade
    flash(_('Lesson {0} deleted.').format(lesson_name))
    db.session.delete(lesson_to_delete)
    db.session.commit()
    return redirect(url_for('lessons.list', jump=grade))


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

    content_list = MaterialType.query.all()
    lesson_content = LessonMaterial.query.filter_by(lesson_id=id)

    if form.validate_on_submit():
        lesson_to_edit.name = form.name.data
        # lesson_to_edit.date = form.date.data
        lesson_to_edit.grade = form.grade.data
        # lesson_to_edit.comments = form.comments.data
        db.session.commit()
        return redirect(url_for('lessons.list'))
    else:
        form.grade.default = lesson_to_edit.grade
        form.name.default = lesson_to_edit.name

    form.process()
    return render_template('edit_lesson.html',form=form,
                            lesson_id=lesson_to_edit.id,
                            lesson_content = lesson_content,
                            content_types=content_list
                            )


### edit route, we need to provide a list of ALL questions as well as
#   those on this test.
@lessons_bp.route('/duplicate/<int:id>', methods=['GET','POST'])
@login_required
def duplicate(id):
    lesson_to_duplicate = Lesson.query.get(id)
    if lesson_to_duplicate==None:
        flash(_('Lesson {0} does not exist.'.format(lesson_name)))
        return redirect(url_for('lesson_list'))

    # first duplicate the lesson
    new_lesson = Lesson(lesson_to_duplicate.name + _(' - Copy'), lesson_to_duplicate.grade)
    db.session.add(new_lesson)
    # db.session.commit()

    for material in lesson_to_duplicate.lesson_materials:
        dup_material = LessonMaterial(material.name,material.content,material.lesson_id,material.material_code)
        dup_material.bonus_available = material.bonus_available
        dup_material.date = material.date
        dup_material.scoring_comment = material.scoring_comment

        dup_material.lesson_id = new_lesson.id

        db.session.add(dup_material)

    db.session.commit()

    s = _('Lesson {0} duplicated.').format(lesson_to_duplicate.name)
    flash(s,category='success')
    return redirect(url_for('lessons.list',jump=new_lesson.grade))


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
