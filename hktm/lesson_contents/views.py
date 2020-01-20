from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required
from hktm import db
from hktm.models import Lesson, LessonMaterial, MaterialType
from hktm.lesson_contents.forms import AddForm

from hktm.lesson_contents.RenderContent_KJRD import RenderContentKJRD
from hktm.lesson_contents.RenderContent_KJTS import RenderContentKJTS
from hktm.lesson_contents.RenderContent_KJWR import RenderContentKJWR
from hktm.lesson_contents.RenderContent_NWRD import RenderContentNWRD
from hktm.lesson_contents.RenderContent_TRCP import RenderContentTRCP
from hktm.lesson_contents.RenderContent_KT36 import RenderContentKT36

content_types = {
    'KJRD' : RenderContentKJRD,
    'KJTS' : RenderContentKJTS,
    'KJWR' : RenderContentKJWR,
    'NWRD' : RenderContentNWRD,
    'TRCP' : RenderContentTRCP,
    'KT36' : RenderContentKT36
}

'''
The lesson contents are managed through these routes, except the intial kanji
test thats added as part of the lesson add interface
'''

lesson_contents_bp = Blueprint('lesson_contents', __name__, template_folder='templates/lesson_contents')


## list route
@lesson_contents_bp.route('/list/<int:lesson_id>')
@login_required
def list(lesson_id):
    '''
    List all the lesson content for a specifis lesson id
    '''
    lessons = Lesson.query.all()
    return render_template('list_lessons.html',lessons=lessons)



## add route
@lesson_contents_bp.route('/add/<int:lesson_id>/<content_code>',methods=['GET','POST'])
@login_required
def add(lesson_id,content_code):
    form = AddForm()

    if form.validate_on_submit():
        content_type = MaterialType.query.get(content_code)
        flash(f'New {content_type.name} Added')
        name = form.name.data
        content = form.content.data
        type = content_code

        new_lesson_content = LessonMaterial(name,content,lesson_id,type)
        db.session.add(new_lesson_content)
        db.session.commit()

        return redirect(url_for('lessons.edit',id=lesson_id))

    return render_template(content_code + '_content.html',form=form, content_type=content_code)


@lesson_contents_bp.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    content_to_delete = LessonMaterial.query.get(id)

    lesson_name = lesson_to_delete.name
    flash(f'Lesson {lesson_name} deleted.')
    db.session.delete(lesson_to_delete)
    db.session.commit()
    return redirect(url_for('lessons.list'))


### edit route, we need to provide a list of ALL questions as well as
#   those on this test.
@lesson_contents_bp.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit(id):
    content_to_edit = LessonMaterial.query.get(id)

    #TODO: get a list of all questions and questions on this test for organizing

    form = AddForm()

    if form.submit.data and form.validate():
        content_to_edit.name = form.name.data
        content_to_edit.content = form.content.data
        db.session.commit()
        return redirect(url_for('lessons.edit',id=content_to_edit.lesson_id))

    # pre-populate for form for editing
    elif request.method == 'GET':
        form.name.default = content_to_edit.name
        form.content.default = content_to_edit.content
        form.process()

        test_content = RenderContentKJTS(content_to_edit.content)

        return render_template(content_to_edit.material_code + '_content.html',form=form, content=content_to_edit.content, content_id=content_to_edit.id, content_type=content_to_edit.material_code)

@lesson_contents_bp.route('/preview_factory/<string:content_code>/', defaults={'content':None}, methods=['GET'])
@lesson_contents_bp.route('/preview_factory/<string:content_code>/<string:content>', methods=['GET'])
@login_required
def preview_factory(content_code, content):
    if content == None:
        return render_template('no_content.html')
    content_type = MaterialType.query.get(content_code)
    lesson_content = content_types.get(content_code,'N/A')(content)
    return render_template('preview_container.html',content_type=content_type,lesson_content=lesson_content)

@lesson_contents_bp.route('/print_factory/<int:content_id>', methods=['GET'])
@login_required
def print_factory(content_id):
    '''
    This will present a 'printable' page with the content rendered out as
    intended.

    Depending on the value of the material/contents 'custom_template' it will
    either call the default print template or a custom template named
    [material_code]_print_container.html in the templates directory
    '''

    content = LessonMaterial.query.get(content_id)
    lesson_content = content_types.get(content.material_code,'N/A')(content.content)
    if content.material.custom_template:
        return render_template(content.material_code+'_print_container.html',content=content,lesson_content=lesson_content)
    else:
        return render_template('print_container.html',content=content,lesson_content=lesson_content)
