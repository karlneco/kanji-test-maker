from hktm import app, db
from flask import render_template
from flask_sqlalchemy import get_debug_queries

from hktm.models import Lesson

@app.route('/')
def index():

    lessons = db.session.query(Lesson).order_by(Lesson.name)
    return render_template('index.html', lessons=lessons)

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
