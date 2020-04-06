import os, sys

PROJECT_DIR = '/var/www/labbook.broukej.cz'
sys.path.insert(0, PROJECT_DIR)


def execfile(filename):
    globals = dict( __file__ = filename )
    exec( open(filename).read(), globals )

activate_this = os.path.join( PROJECT_DIR, 'venv/bin', 'activate_this.py' )
execfile( activate_this )

os.chdir("/var/www/labbook.broukej.cz")
from app import app as application

application.debug = True
