from app import db

class Player(db.Model):
    __tablename__ = 'espn_players_half_ppr'

    rank = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    position = db.Column(db.String(10))
    proj_points = db.Column(db.Float)
    picked = db.Column(db.Integer)


    def __repr__(self):
        return """<Player(
                  rank='{}',
                  name='{}',
                  position='{}',
                  proj_points='{}'
                  picked='{}'
                  )""".format(self.rank,
                              self.name,
                              self.position,
                              self.proj_points,
                              self.picked
                              )

