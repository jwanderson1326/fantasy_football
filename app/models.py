from app import db

class Player(db.Model):
    __tablename__ = 'espn_players_nonppr'

    rank = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    position = db.Column(db.String(10))
    proj_points = db.Column(db.Float)


    def __repr__(self):
        return """<User(
                  rank='{}',
                  name='{}',
                  position='{}',
                  proj_points='{}'
                  )""".format(self.rank,
                              self.name,
                              self.position,
                              self.proj_points
                              )

