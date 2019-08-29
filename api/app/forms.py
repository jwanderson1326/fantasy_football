from flask_wtf import FlaskForm
from wtforms import IntegerField,  SubmitField
from wtforms.validators import DataRequired

class PickForm(FlaskForm):
    rank_num = IntegerField('Rank')
    submit = SubmitField('Pick')
    unsubmit = SubmitField('Unpick')
    reset = SubmitField('Reset')
