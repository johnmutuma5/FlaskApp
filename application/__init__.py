from flask import Flask
from flaskext.mysql import MySQL #remember to inclune mysql_config in the path by sudo apt-get install libmysqlclient-dev

app = Flask (__name__)
app.config.from_object('config')
db = MySQL(app)

from application import views
