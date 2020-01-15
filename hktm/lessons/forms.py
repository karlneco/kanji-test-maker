from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField

## this form witll b e used for adding and editing
class AddForm(FlaskForm):
    name = StringField(u'学期と単元名')
    submit = SubmitField(u'保存する')

class MaterialForm(FlaskForm):
    mat_name = StringField(u'Enter the name of the sheet - this will be on the printerd document')
    mat_content = TextAreaField(u'Here are the questions for this material')
    mat_type = SelectField(u'Content Type', choices=[('KJTS','Kanji Test'),('WRKS','Worksheet'),('KJPR','Kanji Practice')])
    mat_submit = SubmitField(u'Save')
