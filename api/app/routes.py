from flask import render_template, redirect, request, flash
from app import app
from app.forms import PickForm
from config import POSITION_LOOKUP
from manipulations import get_recommendation, pick, unpick, reset, get_current_pick

def get_pos_recommendation(position):
    rec = get_recommendation()
    rec_pos = rec[position]
    return rec_pos

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
def index():
    form = PickForm()
    recs = get_recommendation()
    current_pick = get_current_pick()
    if request.method == 'POST':
        if form.submit.data == True:
            rank = form.rank_num.data
            pick(rank)
        if form.unsubmit.data == True:
            rank = form.rank_num.data
            unpick(rank)
        if form.reset.data == True:
            reset()
        return redirect('/index')
    return render_template('index.html', recs=recs, form=form, current_pick=current_pick)


