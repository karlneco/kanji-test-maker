from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField

## this form witll b e used for adding and editing
class AddForm(FlaskForm):
    name = StringField(u'Enter a descriptive name for the test that can be used to identify it')
    date = StringField(u'Enter the date or date description to display on the worksheets and tests')
    grade = StringField(u'What is the grade level of this test')
    comments = TextAreaField(u'Any additional comments for the test')
    kanji_test = TextAreaField(u'Please enter the Kanji test questions below, one question per line.')
    submit = SubmitField(u'Save Lesson')

class MaterialForm(FlaskForm):
    mat_name = StringField(u'Enter the name of the sheet - this will be on the printerd document')
    mat_content = TextAreaField(u'Here are the questions for this material')
    mat_type = SelectField(u'Content Type', choices=[('KJTS','Kanji Test'),('WRKS','Worksheet'),('KJPR','Kanji Practice')])
    mat_submit = SubmitField(u'Save')
