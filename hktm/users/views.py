from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from hktm import db
from hktm.models import User
from hktm.users.forms import LoginForm, RegistrationForm

users_bp = Blueprint('users', __name__, template_folder='templates/users')

@users_bp.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Account created, please wait for a confirmation email before loging in.')
        return redirect(url_for('hktm.index'))
    return render_template('register.html',form=form)


@users_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('hktm.index'))
