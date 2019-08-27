from math import ceil

from app.models import Player
from app import db
from config import NUMBER_TEAMS, POSITIONS, ROUNDS, PICK

####################################
# Picking Functions
####################################

def pick(rank):
    player = Player.query.filter_by(rank=rank).first()
    player.picked = 1
    db.session.commit()

def unpick(rank):
    player = Player.query.filter_by(rank=rank).first()
    player.picked = 0
    db.session.commit()

def reset():
    for row in Player.query.all():
        row.picked = 0
        db.session.commit()

def get_current_pick():
    curr_pick = Player.query.filter_by(picked=1).count()
    return curr_pick + 1


####################################
# Logisitic Functions
####################################
def get_orig_pick(pick):
    '''Based on a pick, provides your original pick position'''
    round_num = ceil(pick/NUMBER_TEAMS)
    if round_num % 2 == 0:
        if pick % NUMBER_TEAMS == 0:
            orig_pick = 1
        else:
            orig_pick = (NUMBER_TEAMS - ((pick % NUMBER_TEAMS) - 1))
    else:
        if pick % NUMBER_TEAMS == 0:
            orig_pick = 12
        else:
            orig_pick = pick % NUMBER_TEAMS
    return orig_pick


def get_draft_positions(curr_pick, rounds):
    '''Provides a list of your pick numbers'''
    pick = get_orig_pick(curr_pick)
    if pick > NUMBER_TEAMS:
        raise ValueError('Your pick number is higher than # of teams')
    pick_list = []
    for i in range(1, rounds+1):
        if i % 2 != 0:
            pick_number = NUMBER_TEAMS * (i - 1) + pick
        else:
            pick_number = NUMBER_TEAMS * (i - 1) + NUMBER_TEAMS - (pick - 1)
        pick_list.append(pick_number)
    return pick_list

def create_likely_gone():
    current_pick = get_current_pick()
    pick_list = get_draft_positions(current_pick, ROUNDS)
    future_picks = [a for a in pick_list if a >= current_pick]
    picks_before = future_picks[1] - future_picks[0]
    likely_gone_blob = Player.query.filter_by(picked=0).order_by(Player.rank).limit(picks_before).all()
    likely_gone = [player.rank for player in likely_gone_blob]
    return likely_gone


####################################
# Marginal Calculations
####################################

def get_best_player(position):
    best = Player.query.filter_by(picked=0, position=position).order_by(Player.proj_points.desc()).limit(1).first()
    return best


def get_alternative_player(position):
    likely_gone = create_likely_gone()
    alt_player_blob = Player.query.filter_by(picked=0, position=position).order_by(Player.proj_points).all()
    best_alt_rank = [player.rank for player in alt_player_blob if player.rank not in likely_gone].pop()
    alt_player = Player.query.filter_by(rank=best_alt_rank).first()
    return alt_player


def get_recommendation():
    situation = []
    for position in POSITIONS:
        best = get_best_player(position)
        alt = get_alternative_player(position)
        diff = best.proj_points - alt.proj_points
        position_blob = {
            'position' : position,
            'best_name' : best.name,
            'alt_name' : alt.name,
            'diff' : diff
        }
        situation.append(position_blob)
    situation_sorted = sorted(situation, key = lambda i: i['diff'], reverse=True)
    return situation_sorted
