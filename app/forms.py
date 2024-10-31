from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CreateGardenForm(FlaskForm):
    name = StringField('Garden Name', validators=[DataRequired()])
    submit = SubmitField('Create')