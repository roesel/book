# Flask stuff
from flask import Flask, render_template, flash, redirect, escape, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

# DB stuff (to be removed in the future)
import peewee

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

