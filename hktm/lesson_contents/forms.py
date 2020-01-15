from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField

## this form witll b e used for adding and editing
class AddForm(FlaskForm):
    name = StringField(u'Enter the name of the sheet - this will be on the printerd document')
    content = TextAreaField(u'Here are the questions for this material')
    submit = SubmitField(u'Save')
