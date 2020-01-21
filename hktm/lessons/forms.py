from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import InputRequired

## this form witll b e used for adding and editing
class AddForm(FlaskForm):
    name = StringField(u'学期と単元名',validators=[InputRequired(message='This field is required!!!!!')])
    grade = SelectField(u'Grade', choices=[])
    submit = SubmitField(u'保存する')

class MaterialForm(FlaskForm):
    mat_name = StringField(u'Enter the name of the sheet - this will be on the printerd document',validators=[InputRequired(message='This field is required!!!!!')])
    mat_content = TextAreaField(u'Here are the questions for this material')
    mat_type = SelectField(u'Content Type', choices=[('KJTS','Kanji Test'),('WRKS','Worksheet'),('KJPR','Kanji Practice')])
    mat_submit = SubmitField(u'Save')
