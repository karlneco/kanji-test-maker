import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

####################################################
### Flask Setup
####################################################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretsquirrel'


####################################################
### DB Setup
####################################################
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Migrate(app,db)


####################################################
### Blueprints Setup
####################################################
from hktm.questions.views import questions_bp
from hktm.tests.views import tests_bp
from hktm.lessons.views import lessons_bp

app.register_blueprint(questions_bp, url_prefix='/questions')
app.register_blueprint(tests_bp, url_prefix='/tests')
app.register_blueprint(lessons_bp, url_prefix='/lessons')
