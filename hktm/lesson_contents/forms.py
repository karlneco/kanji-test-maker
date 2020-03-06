from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Optional
from flask_babel import lazy_gettext as _

## this form witll b e used for adding and editing
class AddForm(FlaskForm):
    name = StringField(_('Worksheet Title'),validators=[DataRequired()])
    date = StringField(_('Date'))
    bonus = StringField(_('Bonus Score Available',validators=[Optional()]))
    scoring_comment = StringField(_('Scoring Comments'))
    content = TextAreaField(_('Worksheet Content'))
    submit = SubmitField(_('Save'))
