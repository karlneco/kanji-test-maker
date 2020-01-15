from flask import Blueprint, render_template, request, redirect, url_for, flash
from hktm import db
from hktm.models import Lesson, LessonMaterial, MaterialType
from hktm.lessons.forms import AddForm, MaterialForm
from hktm.lesson_contents.RenderContent_KJTS import RenderContentKJTS

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

        new_lesson = Lesson(name)
        db.session.add(new_lesson)
        db.session.flush()
        db.session.refresh(new_lesson)
        db.session.commit()

        return redirect(url_for('lessons.edit',id=new_lesson.id))

    return render_template('add_lesson.html',form=form)


@lessons_bp.route('/delete/<int:id>', methods=['GET'])
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
def edit(id):
    lesson_to_edit = Lesson.query.get(id)

    #TODO: get a list of all questions and questions on this test for organizing

    form = AddForm()

    if form.validate_on_submit():
        lesson_to_edit.name = form.name.data
        # lesson_to_edit.date = form.date.data
        # lesson_to_edit.grade = form.grade.data
        # lesson_to_edit.comments = form.comments.data
        db.session.commit()
        return redirect(url_for('lessons.list'))

    # pre-populate for form for editing
    elif request.method == 'GET':
        #get the different content types to pass to the form
        content_list = MaterialType.query.all()
        lesson_content = LessonMaterial.query.filter_by(lesson_id=id)
        form.name.default = lesson_to_edit.name
        form.process()
    return render_template('edit_lesson.html',form=form,
                            lesson_id=lesson_to_edit.id,
                            lesson_content = lesson_content,
                            content_types=content_list
                            )


@lessons_bp.route('/kanji_test_preview/<string:content>', methods=['GET','POST'])
def kanji_test_preview(content):
    mat = RenderContentKJTS(content)
    return render_template('kanji_test_preview.html',test=mat);


@lessons_bp.route('/kanji_test_print/<string:content>', methods=['GET','POST'])
def kanji_test_pint(content):
    mat = RenderContentKJTS(content)
    return render_template('kanji_test_print.html',test=mat);
