from datetime import datetime

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
    """Each instance of the User model represents a chopstix user."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username=None, email=None):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username