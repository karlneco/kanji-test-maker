from flask import Blueprint, render_template, request, redirect, url_for, flash
from hktm import db
from hktm.models import Lesson, LessonMaterial, MeterialType
from hktm.lesson_contents.forms import AddForm
from hktm.lesson_contents.RenderContent_KJTS import RenderContentKJTS

'''
The lesson contents are managed through these routes, except the intial kanji
test thats added as part of the lesson add interface
'''

lesson_contents_bp = Blueprint('lesson_contents', __name__, template_folder='templates/lesson_contents')


## list route
@lesson_contents_bp.route('/list/<int:lesson_id>')
def list(lesson_id):
    '''
    List all the lesson content for a specifis lesson id
    '''
    lessons = Lesson.query.all()
    return render_template('list_lessons.html',lessons=lessons)



## add route
@lesson_contents_bp.route('/add/<int:lesson_id>/<content_code>',methods=['GET','POST'])
def add(lesson_id,content_code):
    form = AddForm()
    if form.validate_on_submit():
        flash('New Lesson Content Added')
        name = form.name.data
        content = form.content.data
        type = form.type.data

        new_lesson_content = LessonMaterial(name,content,lesson_id,type)
        db.session.add(new_lesson_content)
        db.session.commit()

        return redirect(url_for('lessons.edit',id=new_lesson.id))

    return render_template(content_code + '_content.html',form=form, content_code=content_code)


@lesson_contents_bp.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    lesson_to_delete = Lesson.query.get(id)

    lesson_name = lesson_to_delete.name
    flash(f'Lesson {lesson_name} deleted.')
    db.session.delete(lesson_to_delete)
    db.session.commit()
    return redirect(url_for('lessons.list'))


### edit route, we need to provide a list of ALL questions as well as
#   those on this test.
@lesson_contents_bp.route('/edit/<int:id>', methods=['GET','POST'])
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

        test_content = RenderContentKJTS(kanji_test.content)
    return render_template('edit_lesson.html',form=form, kanji_form=kanji_form, test_content=kanji_test.content, lesson_id=lesson_to_edit.id)


@lesson_contents_bp.route('/preview_factory/<string:content_type>/<string:content>', methods=['GET'])
def preview_factory(content_type, content):
    pass



@lesson_contents_bp.route('/kanji_test_preview/<string:content>', methods=['GET','POST'])
def kanji_test_preview(content):
    mat = ContentKJTS(content)
    return render_template('kanji_test_preview.html',test=mat);


@lesson_contents_bp.route('/kanji_test_print/<string:content>', methods=['GET','POST'])
def kanji_test_pint(content):
    mat = RenderContentKJTS(content)
    return render_template('kanji_test_print.html',test=mat);
