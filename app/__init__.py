from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kjhagsdfjhgasdkjhfgjkhgasaqra'

from flask_login import LoginManager
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, database, access_system