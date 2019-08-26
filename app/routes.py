from app import app
from manipulations import get_recommendation

def get_pos_recommendation(position):
    rec = get_recommendation()
    rec_pos = rec[position]
    return rec_pos

@app.route('/')
@app.route('/index')
def index():
    return '<h1>This is a Fantasy Football App</h1>'


@app.route('/rec')
def recommendation():
    return str(get_recommendation())

@app.route('/rec/rb')
def rec_rb():
    return str(get_pos_recommendation('RB'))

