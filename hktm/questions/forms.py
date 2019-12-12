from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

## this form witll b e used for adding and editing
class AddForm(FlaskForm):
    type = SelectField(u'What type of question is this', choices=[('1','Reading'),('2','Writing'),('3','Combination')])
    grade = StringField(u'What is the grade level of this question')
    question = StringField(u'Enter the question using the appropriate syntax:')
    submit = SubmitField('Save Question')
