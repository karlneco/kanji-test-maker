from hktm import db, login_manager,babel
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_sqlalchemy import get_debug_queries
from flask_login import login_user, login_required, logout_user, current_user
from hktm.models import User
from hktm.users.forms import LoginForm
from hktm.models import Lesson
from flask_babel import _

root_bp = Blueprint('root',__name__, template_folder='templates')

@babel.localeselector
def get_locale():
    return 'ja' #request.accept_languages.best_match(app.config['LANGUAGES'].keys())

@root_bp.route('/',methods=['GET','POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()


        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                if user.grades == 'none':
                    flash(_('Your account has not been activated. You will receive an email once it has been activated'), category="warning")
                    return redirect(url_for('root.index'))
                flash(_('Login Successful'))
                # if user was lookign for a specific page then take them tere now
                next = request.args.get('next')

                if next == None or not next[0]=='/':
                    next = url_for('root.home')

                return redirect(next)
        flash(_('The email address or password is incorrect'), category="danger")
    return render_template('index.html', form=form)


@root_bp.route('/home')
@login_required
def home():

    lessons = db.session.query(Lesson).filter(Lesson.grade.in_(current_user.grades)).order_by(Lesson.name)
    return render_template('home.html', lessons=lessons, user=current_user)


@root_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash(_("You have been logged out"))
    return redirect(url_for('root.index'))


@root_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def sql_debug(response):
    queries = list(get_debug_queries())
    qstr = ''
    for q in queries:
        qstr += str(q.statement % q.parameters).replace('\n','\n        ')

    print ('=' * 80)
    print( 'SQL Queries - {0}'.format(len(queries)))
    print ('=' * 80)
    print (qstr.rstrip('\n'))
    print( '=' * 80 + '\n')

    return response

#app.after_request(sql_debug)
