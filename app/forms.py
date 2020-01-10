from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, HiddenField
from wtforms.validators import DataRequired

class ChooseForm(FlaskForm):
    textU = StringField('Text for upper row:', validators=[DataRequired()])
    textD = StringField('Text for bottom row')
    useD = BooleanField('Use second text')
    fontSize = StringField('Font size')
    field = RadioField('Choose image',
        choices = [('1', 'One'), ('2', 'Two')],
        validators=[DataRequired()])
    submit = SubmitField('Proceed!')

class PreviewForm(FlaskForm):
    left1 = HiddenField('left1')
    left2 = HiddenField('left2')
    top1 = HiddenField('top1')
    top2 = HiddenField('top2')
    submit = SubmitField('Create!')
