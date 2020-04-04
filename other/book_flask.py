#! /usr/bin/env python

from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from datetime import timedelta
from db_demo_func import *
from access_system import *
from collections import OrderedDict

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_name = request.form['name']

        try:
            return redirect(f'/user/{user_name}/')
        except:
            return "Your email seems to not exist in the database"

    else:
        return render_template('index.html')


@app.route('/user/<user_name>/')
def dashboard(user_name):
    try:
        bookings = get_bookings_of_user(user_name)
    except:
        return "Could not retrieve your bookings"
    return render_template('dashboard.html', bookings=bookings, user_name=user_name)


@app.route('/delete/<user_name>/<int:id>/')
def cancel(user_name, id):
    try:
        num_of_deleted_rows = delete_booking(id)
    except:
        return "Could not cancel your booking"
    assert num_of_deleted_rows < 2
    return redirect('/user/{}/'.format(user_name))


@app.route('/user/<user_name>/book/', methods=['POST', 'GET'])
def book(user_name):
    if request.method == 'POST':
        book_room_id = int(request.form.get('rooms'))
        print('Got room ids')
        return redirect(f'/user/{user_name}/book/{book_room_id}/')
    else:
        try:
            rooms = get_all_rooms()
        except:
            return "Could not retireve rooms"
        return render_template('book.html', rooms=rooms, user_name=user_name)


@app.route('/user/<user_name>/book/<int:room_id>/', methods=['POST', 'GET'])
def choose_date(user_name, room_id, methods=['POST', 'GET']):
    now = datetime.now()
    checks = OrderedDict()
    for i in range(7):
        when = now + timedelta(days=i)
        checks[when] = bool(check_bookings_count(when, room_id)[0])

    return render_template('choose_date.html', checks=checks, user_name=user_name, room_id=room_id)


@app.route('/user/<user_name>/book/<int:room_id>/<time>/', methods=['POST', 'GET'])
def book_date(user_name, room_id, time, methods=['GET']):
    _ = create_booking(user_name, time, room_id)
    return redirect(f'/user/{user_name}/')


if __name__ == "__main__":
    app.run(debug=True)
