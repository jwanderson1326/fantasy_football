from app import db

class Player(UserMixin, db.Model):
    __tablename__ = 'players'

    user_id = db.Column(db.String(20), primary_key=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_date = db.Column(db.DateTime())

    activities = db.relationship('Activity', backref='person', lazy='dynamic')

    def __repr__(self):
        return """<User(
                  first_name='{}',
                  last_name='{}',
                  id='{}',
                  email='{}'
                  )""".format(self.first_name,
                              self.last_name,
                              self.user_id,
                              self.email
                              )

