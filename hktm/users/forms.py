from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Emailアドレスを入力してください。', validators=[DataRequired(),Email()])
    password = PasswordField('パスワード',validators=[DataRequired()])
    submit = SubmitField('ログイン')

class AdminAddForm(FlaskForm):
    name = StringField('担任名')
    email = StringField('Emailアドレス', validators=[InputRequired(message='このメールアドレスは正しくありません。'),Email()])
    password = StringField('パスワード', validators=[InputRequired(message='この項目は必須です。')])
    grades = StringField('学年', validators=[InputRequired(message='この項目は必須です。')])
    submit = SubmitField('保存')

class AdminEditForm(FlaskForm):
    name = StringField('担任名')
    email = StringField('Emailアドレス', validators=[InputRequired(message='このメールアドレスは正しくありません。'),Email()])
    password = StringField('パスワード')
    grades = StringField('学年', validators=[InputRequired(message='この項目は必須です。')])
    submit = SubmitField('保存')


class RegistrationForm(FlaskForm):
    email = StringField('Emailアドレスを入力してください。', validators=[InputRequired(message='正しく入力してください。'),Email()])
    password = PasswordField('パスワード',validators=[DataRequired(),EqualTo('password_confirm', message='パスワードが一致しません。')])
    password_confirm = PasswordField('確認のため、もう一度パスワードを入力してください。',validators=[DataRequired()])
    submit = SubmitField('登録する')

    def check_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('このメールアドレスは既に登録済みです。')
