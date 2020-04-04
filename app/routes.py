# Flask stuff
from flask import Flask, render_template, flash, redirect, escape, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

# DB stuff (to be removed in the future)
import peewee

# Other
from datetime import datetime
from datetime import timedelta
from app.database import *
from app.access_system import *
from collections import OrderedDict

# The rest of our app
from app import app
from app.models import User
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            # TODO: move this down to DB layer
            user = User.select().where(User.email == form.email.data).get()
            print(type(user))
        except peewee.DoesNotExist:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        if not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/dashboard/')
def dashboard():
    bookings = get_bookings_of_user(current_user.id)
    print(bookings)
    #try:
    #    bookings = get_bookings_of_user(current_user)
    #except:
    #    return "Could not retrieve your bookings"
    return render_template('dashboard.html', bookings=bookings, user_name=current_user.name)


@app.route('/cancel-booking/<int:id>/')
def cancel_booking(id):
    # TODO: DB: Check for permission (if the current user is allowed to remove this booking)
    try:
        num_of_deleted_rows = delete_booking(id)
    except:
        return "Could not cancel your booking"
    assert num_of_deleted_rows < 2
    return redirect('/dashboard/')

@app.route('/book/', methods=['POST', 'GET'])
def book():
    if request.method == 'POST':
        book_room_id = int(request.form.get('rooms'))
        print('Got room ids')
        return redirect(f'/choose-date/{book_room_id}/')
    else:
        try:
            rooms = get_all_rooms()
        except:
            return "Could not retireve rooms"
        return render_template('book.html', rooms=rooms, user_name=current_user.name)


@app.route('/choose-date/<int:room_id>/', methods=['POST', 'GET'])
def choose_date(room_id):
    # TODO: Merge with existing DB function - get_free_slots(room_id)
    # TODO: Upgrade the DB function to use strftime() - get_free_slots(room_id, start_date, number of days)
    #now = datetime.now()
    #checks = OrderedDict()
    #for i in range(7):
    #    when = now + timedelta(days=i)
    #    checks[when] = bool(check_bookings_count(when, room_id)[0])

    checks = get_free_slots(room_id)

    return render_template('choose_date.html', checks=checks, user_name=current_user.name, room_id=room_id)

@app.route('/make-booking/<int:room_id>/<when>/', methods=['POST', 'GET'])
def make_booking(room_id, when):
    _ = create_booking(current_user.id, when, room_id)
    return redirect(f'/dashboard/')