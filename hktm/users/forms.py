from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from wtforms import ValidationError
from flask_babel import _

class LoginForm(FlaskForm):
    email = StringField(_('Email Address'), validators=[DataRequired(),Email()])
    password = PasswordField(_('Password'),validators=[DataRequired()])
    submit = SubmitField(_('Login'))

class AdminAddForm(FlaskForm):
    name = StringField(_('Teachers Name'))
    email = StringField(_('Teachers Email Address'), validators=[InputRequired(message=_('The Email address is required.')),Email()])
    password = StringField(_('Password'), validators=[InputRequired(message=_('A password is required to create a new user.'))])
    grades = StringField(_('Grade(s)'), validators=[InputRequired(message=_('Please provide a grade or grades for this teacher.'))])
    submit = SubmitField(_('Save'))

class AdminEditForm(FlaskForm):
    name = StringField(_('Teachers Name'))
    email = StringField(_('Teachers Email Address'), validators=[InputRequired(message=_('The Email address is required.')),Email()])
    password = StringField(_('Password'))
    grades = StringField(_('Grade(s)'), validators=[InputRequired(message=_('Please provide a grade or grades for this teacher.'))])
    submit = SubmitField(_('Save'))


class RegistrationForm(FlaskForm):
    email = StringField(_('Email Address'), validators=[InputRequired(message='正しく入力してください。'),Email()])
    password = PasswordField(_('Password'),validators=[DataRequired(),EqualTo('password_confirm', message=_('Password does not match'))])
    password_confirm = PasswordField(_('Re-Enter Password'),validators=[DataRequired()])
    submit = SubmitField(_('Register...'))

    def check_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError(_('This email address is already registered'))
