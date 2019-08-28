from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField
from wtforms.validators import DataRequired

class PickForm(FlaskForm):
    rank_num = StringField('Rank', validators=[DataRequired()])
    submit = SubmitField('Pick')
