from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Re-Enter Password',validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('This email is already registered')
