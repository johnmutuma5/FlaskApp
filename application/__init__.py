from flask import Flask
from flaskext.mysql import MySQL #remember to inclune mysql_config in the path by sudo apt-get install libmysqlclient-dev
from WSGI_middleware import WSGI_app

app = Flask (__name__)
app.config.from_object('config')
db = MySQL(app)

app = WSGI_app(app)

from application import views
