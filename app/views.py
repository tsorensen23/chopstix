import json, datetime
from datetime import timedelta

from flask import render_template, flash, redirect, session, url_for, request, g, Response
from flask.ext.login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc

from app import app, db, lm, oid
from forms import LoginForm
from models import User, Ticket, ROLE_USER, ROLE_ADMIN

@app.route('/')
@app.route('/index')
@login_required

def index():
    user = g.user
    posts = [
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
        title = 'Home',
        user = user,
        posts = posts)

@app.route('/show_fake_tickets/')
def show_entries():
    """The main view of this app. Display all the tickets for sale."""
    return render_template('show_entries.html')

@app.route('/add_ticket/')
def add_ticket():
    """Add a single new ticket to the database"""
    ticket = Ticket(game='Tom v. Travis',
                    section='12',
                    game_day=datetime.datetime.now() - timedelta(days=15),
                    row='32',
                    seat_no='3')
    db.session.add(ticket)
    db.session.commit()
    return 'Ticket Added successfully!!!'

@app.route('/data/tickets/')
def show_tickets():
    """Return json data for all tickets to be displayed."""

    tickets = Ticket.query.order_by(Ticket.game_day).all()
    #for ticket in tickets:
        #print ticket
    return return_json(tickets)

def return_json(tickets):
    payload = []
    for ticket in tickets:
        print ticket.game_day
        weekdaynum = ticket.game_day.weekday()
        weekdaylist = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday = weekdaylist[weekdaynum]
        month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
        game_day = ticket.game_day.day
        print '#######'
        print dir(ticket.game_day)
        month_num = ticket.game_day.month
        game_month = month_list[month_num]
        ticket_dict = {'game': ticket.game,
                       'weekday': weekday,
                       'game_day': game_day,
                       'game_month': game_month,
                       'row': ticket.row,
                       'seat_no': ticket.seat_no,
                       'section': ticket.section,
                       'seller': 'Deon W.',
                       'price': 35,
        }
        payload.append(ticket_dict)

    return Response(json.dumps(payload), mimetype='application/json')

@app.route('/data/tickets_future/')
def data_tickets_future():
    """Return json data for all tickets to be displayed."""

    tickets = Ticket.query.filter(Ticket.game_day >= datetime.datetime.now()).order_by(Ticket.game_day)

    return return_json(tickets)


@app.route('/data/tickets_past/')
def data_tickets_past():
    """Return json data for all tickets to be displayed."""

    tickets = Ticket.query.filter(Ticket.game_day <= datetime.datetime.now()).order_by(desc(Ticket.game_day))

    return return_json(tickets)


@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))