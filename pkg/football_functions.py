from math import ceil

from .config import NUMBER_TEAMS, POSITIONS, ROUNDS, PICK
from .utils.db_functions import connect_to_db


def get_orig_pick(pick):
    round_num = ceil(pick/NUMBER_TEAMS)
    if round_num % 2 == 0:
        orig_pick = (NUMBER_TEAMS - ((pick % NUMBER_TEAMS) - 1))
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
    db = connect_to_db()
    curs = db.cursor()
    curs.execute("drop table if exists likely_gone")
    curs.execute("create table if not exists likely_gone as \
                select * from player where picked is null \
                order by rank limit %d" % picks_before)
    db.commit()
    curs.close()


################################################
#Picking functions
################################################
def reset_picks():
    db = connect_to_db()
    curs = db.cursor()
    curs.execute("UPDATE player SET picked = NULL")
    db.commit()
    curs.close()


def pick(rank):
    db = connect_to_db()
    curs = db.cursor()
    curs.execute("UPDATE player SET picked = 'y' where rank = %d" % rank)
    db.commit()
    curs.close()


def unpick(rank):
    db = connect_to_db()
    curs = db.cursor()
    curs.execute("UPDATE player SET picked = NULL where rank = %d" % rank)
    db.commit()
    curs.close()


def get_current_pick():
    db = connect_to_db()
    curs = db.cursor()
    curs.execute("SELECT count(*) FROM player where picked = 'y'")
    pick = curs.fetchone()[0] + 1
    curs.close()
    return pick




#########################################
#Marginal Calculations
#########################################

def get_best_player(position):
    db = connect_to_db()
    curs = db.cursor()
    curs.execute('SELECT * FROM player where pos="%s" and picked is null order by pts desc limit 1' % position)
    player = curs.fetchone()
    curs.close()
    return player


def get_alternative_player(position):
    create_likely_gone()
    db = connect_to_db()
    curs = db.cursor()
    curs.execute('SELECT * FROM player where pos="%s" and picked is null \
                 and rank not in (select rank from likely_gone) \
                 order by pts desc limit 1' % position)
    player = curs.fetchone()
    curs.close()
    return player


def get_recommendation():
    situation = []
    for position in POSITIONS:
        best = get_best_player(position)
        alt = get_alternative_player(position)
        rec_name = best[2]
        alt_name = alt[2]
        diff = best[1] - alt[1]
        situation.append([position, rec_name, alt_name, diff])
    situation.sort(key=lambda x: x[3], reverse=True)
    for i in situation:
        print(i[0])
        print('Rec: %s' % i[1])
        print('Alt: %s' % i[2])
        print('Cost: %d' % i[3])
    return situation
