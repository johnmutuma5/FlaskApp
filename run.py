#!flaskapp/bin/python

from application import app

#run this when this file is main
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 5000, app, use_debugger=True, use_reloader=True)
