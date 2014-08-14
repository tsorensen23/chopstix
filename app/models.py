from datetime import datetime

from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class Ticket(db.Model):
    """Each instance of the Ticket model represents a ticket for sale."""
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(80))
    section = db.Column(db.String(10))
    row = db.Column(db.String(10))
    seat_no = db.Column(db.String(10))
    created_on = db.Column(db.DateTime)

    def __init__(self, game=None, section=None, row=None, seat_no=None, created_on=None):
        self.game = game
        self.section = section
        self.row = row
        self.seat_no = seat_no
        if created_on is None:
            created_on = datetime.utcnow()
        self.created_on = created_on

    def __repr__(self):
        return '<Ticket %r>' % self.game

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)