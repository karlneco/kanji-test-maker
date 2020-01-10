from flask import Blueprint, render_template, request, redirect, url_for, flash
from hktm import db
from hktm.models import Lesson, LessonMaterial
from hktm.lessons.forms import AddForm, MaterialForm
from hktm.lessons.content_KJTS import ContentKJTS

lessons_bp = Blueprint('lessons', __name__, template_folder='templates/lessons')
## list route
@lessons_bp.route('/list')
def list():
    lessons = Lesson.query.all()
    return render_template('list_lessons.html',lessons=lessons)



## add route
@lessons_bp.route('/add',methods=['GET','POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        flash('New Lesson Created')
        name = form.name.data
        date = form.date.data
        grade = form.grade.data
        comments = form.comments.data
        kanji_test = form.kanji_test.data


        new_lesson = Lesson(name,date,grade,comments)
        db.session.add(new_lesson)
        db.session.flush()
        db.session.refresh(new_lesson)

        new_material = LessonMaterial(name+' '+date, kanji_test,new_lesson.id,'T')
        db.session.add(new_material)
        db.session.commit()

        return redirect(url_for('lessons.edit',id=new_lesson.id))

    return render_template('add_lesson.html',form=form)



### edit route, we need to provide a list of ALL questions as well as
#   those on this test.
@lessons_bp.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    lesson_to_edit = Lesson.query.get(id)

    #TODO: get a list of all questions and questions on this test for organizing

    form = AddForm()
    kanji_form = MaterialForm()

    if form.submit.data and form.validate():
        lesson_to_edit.name = form.name.data
        lesson_to_edit.date = form.date.data
        lesson_to_edit.grade = form.grade.data
        lesson_to_edit.comments = form.comments.data
        db.session.commit()
        return redirect(url_for('lessons.list'))

    if kanji_form.mat_submit.data and kanji_form.validate():
        lesson_to_edit.lesson_materials[0].name = kanji_form.mat_name.data
        lesson_to_edit.lesson_materials[0].content = kanji_form.mat_content.data
        db.session.commit()
        return redirect(url_for('lessons.list'))

    # pre-populate for form for editing
    elif request.method == 'GET':
        form.name.default = lesson_to_edit.name
        form.date.default = lesson_to_edit.date
        form.grade.default = lesson_to_edit.grade
        form.comments.default = lesson_to_edit.comments
        kanji_test = lesson_to_edit.lesson_materials[0]
        kanji_form.mat_name.default = kanji_test.name
        kanji_form.mat_type.default = kanji_test.material_code
        kanji_form.mat_content.default = kanji_test.content
        form.process()
        kanji_form.process()

        test_content = ContentKJTS(kanji_test.content)
    return render_template('edit_lesson.html',form=form, kanji_form=kanji_form, test_content=test_content)
