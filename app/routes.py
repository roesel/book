# Flask stuff
from flask import Flask, render_template, flash, redirect, escape, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

# DB stuff (to be removed in the future)
import peewee

# Other
from datetime import datetime
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
    try:
       bookings = get_bookings_of_user(current_user.id)
    except:
       return "Could not retrieve your bookings"
    return render_template('dashboard.html', bookings=bookings, user_name=current_user.name, prettify_when=prettify_when)


@login_required
@app.route('/manage/')
def manage():
   
    bookings = get_pending_bookings()
    #try:
    #   bookings = get_pending_bookings(current_user.id)
    #except:
    #   return "Could not retrieve your bookings"
    
    # for b in bookings:
        # b["user"] = 'Honeybadger'
    return render_template('manage.html', bookings=bookings, user_name=current_user.name, prettify_when=prettify_when)

@app.route('/deny-booking/<int:id>/')
def deny_booking_id(id):
    params = get_booking_text(id)
    flash(f'The booking of the room {params[0]} on {params[1]} for {params[2]} was denied.') 
    # TODO: DB: Check for permission (if the current user is allowed to remove this booking)
    success = deny_booking(id)
    if success:
        pass
    return redirect('/manage/')

@app.route('/approve-booking/<int:id>/')
def approve_booking_id(id):
    params = get_booking_text(id)
    flash(f'The booking of the room {params[0]} on {params[1]} for {params[2]} was approved.') 
    # TODO: DB: Check for permission (if the current user is allowed to remove this booking)
    success = approve_booking(id)
    if success:
        pass    
    return redirect('/manage/')

@app.route('/cancel-booking/<int:id>/')
def cancel_booking(id):
    params = get_booking_text(id)
    flash(f'The booking of the room {params[0]} on {params[1]} for {params[2]} was canceled.') 
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
            rooms = get_accessible_rooms(current_user.id)
        except:
            return "Could not retireve rooms"
        return render_template('book.html', rooms=rooms, user_name=current_user.name)

from random import randint
from calendar import Calendar

def checks_to_calendar_days(checks):
    ## Generate input data for calendar
    # TODO: This needs to be done MUCH better
    now = datetime.strptime(checks[0]['when'], '%Y-%m-%d')
    cal = Calendar(0)
    pick_checks = False
    i = -1
    days = []
    for day in cal.itermonthdates(now.year, now.month):
        if now.date() + timedelta(6) >= day >= now.date():
            pick_checks = True
            i += 1
        days.append({
            'day_number': day.day,
            'when': [day.strftime('%Y-%m-%d') + '-AM', day.strftime('%Y-%m-%d') + '-PM'],
            'outside': True if day.month != now.month else False,
            'code': checks[i]['code'] if pick_checks else None,
            'reasons': checks[i]['reasons'] if pick_checks else None,
            'blocked': False if pick_checks else True
        })
        pick_checks = False

    return days

    # Dummy
    # days = [
    #     {
    #         'day_number': i,
    #         'when': '2020-03-{:02d}'.format(i),
    #         'outside': True,
    #         'available': 0,
    #         'blocked': True
    #     }
    #     for i in range(29, 31)
    # ]
    # days = days + [
    #     {
    #         'day_number': i,
    #         'when': '2020-03-{:02d}'.format(i),
    #         'outside': False,
    #         'available': [randint(-1, 2) for i in range(2)],
    #         'blocked': False,
    #         'reasons': [[bool(randint(0, 1)) for i in range(3)] for k in range(2)]
    #     }
    #     for i in range(1, 31)
    # ]
    # days = days + [
    #     {
    #         'day_number': i,
    #         'when': '2020-04-{:02d}'.format(i),
    #         'outside': True,
    #         'available': 0,
    #         'blocked': True
    #     }
    #     for i in range(1, 3)
    # ]

    # Another dummy
    # days = []
    # days.append({'day_number':29, 'when':'2020-03-{:02d}'.format(29), 'outside':True, 'available':False, 'blocked':True})
    # days.append({'day_number':30, 'when':'2020-03-{:02d}'.format(30), 'outside':True, 'available':False, 'blocked':True})
    # for i in range(31):
    #     days.append({'day_number':i+1, 'when':'2020-04-{:02d}'.format(i+1), 'outside':False, 'available':False, 'blocked':True})
    # for j in range(2):
    #     days.append({'day_number':j+1, 'when':'2020-05-{:02d}'.format(j+1), 'outside':True, 'available':False, 'blocked':True})
    # # I will go into algorithm hell for this :(
    # for d in days:
    #     for c in checks:
    #         if d["when"]==c["when"]:
    #             d['blocked'] = False
    #             d['reasons'] = c["reasons"]
    #             if c["available"]:
    #                 d["available"] = True
    # return days

@app.route('/choose-date/<int:room_id>/', methods=['POST', 'GET'])
def choose_date(room_id):
    now = datetime.now()
    checks = get_free_slots_for_user(current_user.id, room_id, now, 7)

    ## Generate input data for calendar
    days = checks_to_calendar_days(checks)
    
    return render_template('choose_date.html', checks=checks, user_name=current_user.name, room_id=room_id, days=days)

from pprint import pprint

@app.route('/calendar/<int:room_id>/', methods=['POST', 'GET'])
def calendar(room_id):
    now = datetime.now()
    checks = get_free_slots_for_user(current_user.id, room_id, now, 7)
    for check in checks:
        pprint(checks)
    days = checks_to_calendar_days(checks)
    # for day in days:
    #     print(day)

    return render_template('calendar.html', checks=checks, user_name=current_user.name, room_id=room_id, days=days)

@app.route('/make-booking/<int:room_id>/<when>/', methods=['POST', 'GET'])
def make_booking(room_id, when):
    _ = create_booking(current_user.id, when, room_id)
    return redirect(f'/dashboard/')

@app.route('/status/', defaults={'when': '2020-04-05'})
@app.route('/status/<when>/')
def status(when):
    
    stats = stats_for_plot_buildings(when)

    #get_plot_code

    print(stats)

    labels_string = '","'.join(stats["labels"])
    
    colors_string_am = '","'.join(stats["colors_AM"])
    data_string_am = ','.join([str(x) for x in stats["data_AM"]])
    label_string_am = stats["label_AM"]
    
    colors_string_pm = '","'.join(stats["colors_PM"])
    data_string_pm = ','.join([str(x) for x in stats["data_PM"]])
    label_string_pm = stats["label_PM"]
    
    text_string = stats["text"]

    plot_code = '''<script>
    // Bar chart
    new Chart(document.getElementById("bar-chart"), {
        type: 'bar',
        data: {
        labels: ["'''+labels_string+'''"],
        datasets: [
            {
            label: "'''+label_string_am+'''",
            backgroundColor: ["'''+colors_string_am+'''"],
            data: ['''+data_string_am+''']
            },
            {
            label: "'''+label_string_pm+'''",
            backgroundColor: ["'''+colors_string_pm+'''"],
            data: ['''+data_string_pm+''']
            }
        ]
        },
        options: {
            title: {
                display: true,
                text: "'''+text_string+'''"
            },
            legend: {
                display: false,
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        stepSize: 1
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Number of people (-)'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Building'
                    }
                }]
            }
        }
    });
    </script>'''
    
    # Date loginc for next/previous
    current_date = datetime.strptime(when, '%Y-%m-%d')
    next_date = current_date + timedelta(days=1)
    prev_date = current_date + timedelta(days=-1)
    next_when = next_date.strftime('%Y-%m-%d')
    prev_when = prev_date.strftime('%Y-%m-%d')
    pretty_date = prettify_date(when)
    
    # Limits
    limits = get_limits()

    return render_template('status.html', stats=stats, plot_code=plot_code, when=when, 
                            pretty_date=pretty_date, prev_when=prev_when, next_when=next_when,
                            limits=limits)


@app.route('/status2/', defaults={'building': 'BM', 'month':'4'})
@app.route('/status2/<building>/<month>/')
def status2(building, month):
    
    stats = stats_for_plot_time(building, int(month))

    print(stats)

    labels_string = '","'.join(stats["labels"])
    
    colors_string_am = '","'.join(stats["colors_AM"])
    data_string_am = ','.join([str(x) for x in stats["data_AM"]])
    label_string_am = stats["label_AM"]
    
    colors_string_pm = '","'.join(stats["colors_PM"])
    data_string_pm = ','.join([str(x) for x in stats["data_PM"]])
    label_string_pm = stats["label_PM"]
    
    text_string = stats["text"]
    x_axis_string = stats["under_text"]

    plot_code = '''<script>
    // Bar chart
    new Chart(document.getElementById("bar-chart"), {
        type: 'bar',
        data: {
        labels: ["'''+labels_string+'''"],
        datasets: [
            {
            label: "'''+label_string_am+'''",
            backgroundColor: ["'''+colors_string_am+'''"],
            data: ['''+data_string_am+''']
            },
            {
            label: "'''+label_string_pm+'''",
            backgroundColor: ["'''+colors_string_pm+'''"],
            data: ['''+data_string_pm+''']
            }
        ]
        },
        options: {
            title: {
                display: true,
                text: "'''+text_string+'''"
            },
            legend: {
                display: false,
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        stepSize: 1
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Number of people (-)'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: "'''+x_axis_string+'''"
                    }
                }]
            }
        }
    });
    </script>'''
    
    # Date loginc for next/previous
    #current_date = datetime.strptime(when, '%Y-%m-%d')
    #next_date = current_date + timedelta(days=1)
    #prev_date = current_date + timedelta(days=-1)
    #next_when = next_date.strftime('%Y-%m-%d')
    #prev_when = prev_date.strftime('%Y-%m-%d')
    #pretty_date = prettify_date(when)
    
    # Limits
    #limits = get_limits()

    return render_template('status2.html', stats=stats, plot_code=plot_code, building=building)


@app.route('/team_info/')
def team_info():
 
    return render_template('team_info.html')
