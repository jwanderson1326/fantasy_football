from flask import render_template, redirect
from app import app
from app.forms import PickForm
from config import POSITION_LOOKUP
from manipulations import get_recommendation

def get_pos_recommendation(position):
    rec = get_recommendation()
    rec_pos = rec[position]
    return rec_pos

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
def index():
    form = PickForm()
    recs = get_recommendation()
    return render_template('index.html', recs=recs, form=form)


