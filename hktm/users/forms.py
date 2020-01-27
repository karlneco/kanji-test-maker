from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log In')

class AdminAddForm(FlaskForm):
    name = StringField('Teacher Name')
    email = StringField('Email', validators=[InputRequired(message='This field is required!!!!!'),Email()])
    password = StringField('Password', validators=[InputRequired(message='This field is required!!!!!')])
    grades = StringField('Grades', validators=[InputRequired(message='This field is required!!!!!')])
    submit = SubmitField('Save')

class AdminEditForm(FlaskForm):
    name = StringField('Teacher Name')
    email = StringField('Email', validators=[InputRequired(message='This field is required!!!!!'),Email()])
    password = StringField('Password')
    grades = StringField('Grades', validators=[InputRequired(message='This field is required!!!!!')])
    submit = SubmitField('Save')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(message='This field is required!!!!!'),Email()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Re-Enter Password',validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('This email is already registered')
