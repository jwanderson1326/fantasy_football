from flask import render_template
from app import app
from config import POSITION_LOOKUP
from manipulations import get_recommendation

def get_pos_recommendation(position):
    rec = get_recommendation()
    rec_pos = rec[position]
    return rec_pos

@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    rec = str(get_recommendation())
    return render_template('index.html', rec=rec)


@app.route('/rec', methods = ['GET'])
def recommendation():
    return str(get_recommendation())

@app.route('/rec/<pos>', methods = ['GET'])
def rec_pos(pos):
    arg = POSITION_LOOKUP[pos]
    return str(get_pos_recommendation(arg))

