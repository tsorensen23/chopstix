""" TODO:
* install post-install hook for bower install
* configure a settings file for production
"""


import json

from flask import Flask, render_template, Response
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from models import db, User, Ticket

# App create/config.
app = Flask(__name__)
app.config.from_object('settings')
db.init_app(app)
admin = Admin(app)

# Admin views
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Ticket, db.session))

@app.route('/')
def show_entries():
    """The main view of this app. Display all the tickets for sale."""
    return render_template('show_entries.html')

@app.route('/data/tickets/')
def show_tickets():
    """Return json data for all tickets to be displayed."""
    tickets = Ticket.query.all()
    print dir(tickets)

    payload = []
    for ticket in tickets:
        ticket_dict = {'game': ticket.game,
                       'row': ticket.row,
                       'seat_no': ticket.seat_no,
                       'section': ticket.section,
                       'seller': 'Deon W.',
                       'price': 35,
        }
        payload.append(ticket_dict)

    return Response(json.dumps(payload), mimetype='application/json')

@app.route('/testdb')
def testdb():
    """A test function to determine whether the databased is attached
    properly
    """
    if db.session.query("1").from_statement("SELECT 1").all():
        return 'It works.'
    else:
        return 'Something is broken.'


if __name__ == "__main__":
    app.run()