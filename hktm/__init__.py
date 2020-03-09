import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel, gettext

####################################################
### Config
####################################################
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'root.index'
babel = Babel()

####################################################
### App Factory
####################################################
def create_app(cf=None):
    print("config at: " + cf)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(cf)
    initialize_extensions(app)
    register_blueprints(app)
    babel.init_app(app)
    #migration support
    Migrate(app,db)

    return app


# attach app
def initialize_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


# load blue  prints
def register_blueprints(app):
    from hktm.lessons.views import lessons_bp
    from hktm.lesson_contents.views import lesson_contents_bp
    from hktm.users.views import users_bp
    from hktm.worksheets.views import worksheets_bp
    from hktm.views import root_bp

    app.register_blueprint(lessons_bp, url_prefix='/lessons')
    app.register_blueprint(lesson_contents_bp, url_prefix='/lesson_contents')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(worksheets_bp, url_prefix='/worksheets/')
    app.register_blueprint(root_bp,url_prefix='/')
    from hktm import views
