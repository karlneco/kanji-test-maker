from hktm import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_sqlalchemy import get_debug_queries
from flask_login import login_user, login_required, logout_user
from hktm.models import User
from hktm.users.forms import LoginForm

from hktm.models import Lesson

@app.route('/',methods=['GET','POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Login Successful')

            # if user was lookign for a specific page then take them tere now
            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('home')

        return redirect(next)

    return render_template('index.html', form=form)


@app.route('/home')
@login_required
def home():

    lessons = db.session.query(Lesson).order_by(Lesson.name)
    return render_template('home.html', lessons=lessons)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('index'))


@app.errorhandler(404)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
