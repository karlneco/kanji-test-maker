from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from hktm import db
from hktm.models import User
from hktm.users.forms import LoginForm, RegistrationForm, AdminEditForm, AdminAddForm
from flask_babel import _

users_bp = Blueprint('users', __name__, template_folder='templates/users')


@users_bp.route('/list')
@login_required
def admin_list_users():
    if 'A' not in current_user.grades:
        flash(_('This functionality is only available to Administrators'), category='danger')
        return redirect(url_for('root.home'))

    all_users = db.session.query(User).all()
    return render_template('list.html', users=all_users)


@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(current_user.id)
    form = AdminEditForm()
    del form.email
    del form.grades

    if form.validate_on_submit():
        user.name = form.name.data
        if form.password.data != "":
            user.password = generate_password_hash(form.password.data)

        db.session.commit()
        return redirect(url_for('users.profile'))
    else:
        form.name.default = user.name
        form.process()

    return render_template('my_profile.html', form=form, user_id=user.id)


@users_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_user_edit(id):
    if 'A' not in current_user.grades:
        flash(_('This functionality is only available to Administrators'), category='danger')
        return redirect(url_for('root.home'))

    user = User.query.get(id)
    form = AdminEditForm()

    if request.method == 'GET':
        form.name.default = user.name
        form.email.default = user.email
        form.grades.default = user.grades
        form.process()

    if form.validate_on_submit():
        user.name = form.name.data
        user.grades = form.grades.data
        if form.password.data != "":
            user.password = generate_password_hash(form.password.data)

        db.session.commit()
        return redirect(url_for('users.admin_list_users'))
    else:
        form.name.default = user.name
        form.email.default = user.email
        form.grades.default = user.grades
        form.process()

    return render_template('admin_user_edit.html', form=form, user_id=user.id)

    user.email = form.email.data


@users_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if 'A' not in current_user.grades:
        flash(_('This functionality is only available to Administrators'), category='danger')
        return redirect(url_for('root.home'))

    form = AdminAddForm()
    if form.validate_on_submit():
        new_user = User(form.email.data, form.password.data)
        new_user.name = form.name.data
        new_user.grades = form.grades.data

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('users.admin_list_users'))

    return render_template('admin_user_add.html', form=form)


@users_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    if 'A' not in current_user.grades:
        flash(_('This functionality is only available to Administrators'), category='danger')
        return redirect(url_for('root.home'))

    user_to_delete = User.query.get(id)

    user_email = user_to_delete.email
    user_name = user_to_delete.name
    flash(_('The teacher ') + user_name + '(' + ''.join(user_email) + ')' + _(' has been deleted'), category='info')
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('users.admin_list_users'))


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        check_user = User.query.filter_by(email=form.email.data).first()
        if isinstance(check_user, User):
            flash(_('This email address is already registered'), category='danger')
            return redirect(url_for('root.index'))

        else:
            user = User(email=form.email.data,
                        password=form.password.data)

            db.session.add(user)
            db.session.commit()

            flash(
                _('Your account have been created.  You will recieve an email once it has been validated and activated. Thank you.'),
                category='warning')
            return redirect(url_for('root.index'))
    return render_template('register.html', form=form)


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('root.index'))
