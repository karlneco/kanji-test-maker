from hktm import app
from flask import render_template

@app.route('/')
def index():
    question_count = 100
    test_count = 4
    return render_template('index.html', question_count=question_count,test_count=test_count)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
