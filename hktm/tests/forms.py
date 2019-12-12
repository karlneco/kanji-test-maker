from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField

## this form witll b e used for adding and editing
class AddForm(FlaskForm):
    name = StringField(u'Enter a descriptive name for the test that can be used to identify it')
    grade = StringField(u'What is the grade level of this test')
    comments = TextAreaField(u'Any additional comments for the test')
    submit = SubmitField(u'Save Test')
