from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required,current_user
from hktm import db
from hktm.models import MaterialType
from hktm.worksheets.forms import AddForm
from flask_babel import _

worksheets_bp = Blueprint('worksheets', __name__, template_folder='templates/worksheets')

def is_admin():
    if 'A' not in current_user.grades:
        flash(_('This functionality is only available to Administrators'), category='danger')
        return False
    return True

## list route
@worksheets_bp.route('/list')
@login_required
def list():
    #check for admin
    if not(is_admin):
        return redirect(url_for('root.home'))

    #get a list of all worksheets - the template will tabetise them
    worksheets = db.session.query(MaterialType).order_by(MaterialType.name)
    return render_template('list_worksheets.html',worksheets=worksheets)



## add route
@worksheets_bp.route('/add',methods=['GET','POST'])
@login_required
def add():
    #check for admin
    if not(is_admin):
        return redirect(url_for('root.home'))

    form = AddForm()

    if form.validate_on_submit():
        code = form.code.data
        name = form.name.data
        instructions = form.instructions.data
        new_ws = MaterialType(code, name, instructions)
        new_ws.custom_template = form.custom.data
        db.session.add(new_ws)
        db.session.commit()
        flash(_('New Worksheet Type created'))
        return redirect(url_for('worksheets.edit',code=new_ws.code))


    return render_template('add_worksheet.html',form=form)


@worksheets_bp.route('/delete/<string:code>', methods=['GET'])
@login_required
def delete(code):

    #check for admin
    if not(is_admin):
        return redirect(url_for('root.home'))

    ws_to_delete = MaterialType.query.get(id)

    name = ws_to_delete.name
    flash(_('Worksheet {0} has been deleted'.format(name)))
    db.session.delete(ws_to_delete)
    db.session.commit()
    return redirect(url_for('worksheets.list'))


### edit route, we need to provide a list of ALL questions as well as
#   those on this test.
@worksheets_bp.route('/edit/<string:code>', methods=['GET','POST'])
@login_required
def edit(code):
    #check for admin
    if not(is_admin):
        return redirect(url_for('root.home'))

    ws_to_edit = MaterialType.query.get(code)

    form = AddForm()

    if form.validate_on_submit():
        ws_to_edit.code = form.code.data
        ws_to_edit.name = form.name.data
        ws_to_edit.instructions = form.instructions.data
        ws_to_edit.custom_template = form.custom.data
        db.session.commit()
        return redirect(url_for('worksheets.list'))
    else:
        form.code.default = ws_to_edit.code
        form.name.default = ws_to_edit.name
        form.instructions.default = ws_to_edit.instructions
        form.custom.default = ws_to_edit.custom_template
        form.process()
    return render_template('edit_worksheet.html',form=form,
                            worksheet_id=ws_to_edit.code)
