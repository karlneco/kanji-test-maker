from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired

## this form witll b e used for adding and editing
class AddForm(FlaskForm):
    name = StringField(u'ページタイトルを記載してください',validators=[DataRequired()])
    content = TextAreaField(u'問題を作成してください')
    submit = SubmitField(u'保存')
