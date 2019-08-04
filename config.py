import os

#DB Configs
HOST = 'localhost'
USER = 'root'
DB = 'football'
PASSWD = 'pass'


DB_URI = "postgresql://{}:{}@{}/{}".format(USER,PASSWD,HOST,DB)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'pass'
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

'''Configurations for draft'''

NUMBER_TEAMS = 12
ROUNDS = 16
PICK = 1

POSITIONS = ['QB',
             'RB',
             'WR',
             'TE',
             'K',
             'D/ST'
             ]



