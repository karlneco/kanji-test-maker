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
def create_app(config_filename=None):
    print("config at: " + config_filename)
    app = Flask(__name__, instance_relative_config=True)

    if config_filename:
        # Load the specified configuration file
        app.config.from_pyfile(config_filename)

    # Check if we are in testing mode
    if app.config.get('TESTING', False):
        # Use a default secret key for testing
        app.config['SECRET_KEY'] = 'test-secret-key'
    else:
        # Override the SECRET_KEY with the value from the environment variable
        secret_key = os.getenv('SECRET_KEY')
        if not secret_key:
            raise RuntimeError('SECRET_KEY environment variable is not set. The application cannot start without it.')
        app.config['SECRET_KEY'] = secret_key

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)

    # Set up login manager settings
    login_manager.login_view = 'staff.staff_login'
    login_manager.login_message = "Please log in to access the requested resource."
    login_manager.login_message_category = "info"

    # Initialize models
    from hktm import models

    # Register blueprints
    register_blueprints(app)

    # Register custom CLI commands
    register_commands(app)

    return app


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
    app.register_blueprint(root_bp, url_prefix='/')
    from hktm import views


def register_commands(app):
    @app.cli.command("create-admin")
    def create_admin():
        """Create the default admin user."""
        from hktm.models import User  # Make sure this import is inside the function to avoid early import issues
        admin_email = "admin@example.com"
        default_password = "admin123"

        # Check if the admin user already exists
        existing_admin = User.query.filter_by(email=admin_email).first()
        if not existing_admin:
            new_admin = User(
                email=admin_email,
                password=default_password,
                # name="Default Admin",
                # grades="A123456789"
            )
            db.session.add(new_admin)
            db.session.commit()
            print("Default admin user created")
        else:
            print("Admin user already exists")
