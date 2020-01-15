from hktm import app
from flask import render_template
from hktm.models import Lesson

@app.route('/')
def index():
    lessons = Lesson.query.all()
    return render_template('index.html', lessons=lessons)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
