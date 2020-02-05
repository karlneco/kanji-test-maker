from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField, BooleanField
from wtforms.validators import InputRequired,Length
from flask_babel import lazy_gettext as _

## this form witll b e used for adding and editing
class AddForm(FlaskForm):
    name = StringField(_('Worksheet Type Name'),validators=[InputRequired(message=_('The Worksheet Type Name is required'))])
    code = StringField(_('Worksheet Code'),validators=[InputRequired(message=_('The Worksheet Code is required')),Length(min=4, max=4)])
    instructions = TextAreaField(_('Worksheet instructions (these will be displayed on the worksheet)'))
    custom = BooleanField(_('Use Custom Template (includes date)'))
    submit = SubmitField(_('Save'))
