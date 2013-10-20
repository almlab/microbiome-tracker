import json
import os
import sys
import base64
path = os.path.dirname(os.path.realpath(__file__))+'/photos/'
sys.path.append(path)

#from flask import Flask, render_template, request

# from flaskr
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE='/tmp/flaskr.db',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return redirect(url_for('photo'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))





def new_file_name(i = 0):
    location = 'photos/'+str(i)+'.jpg'
    if os.path.exists(location):
        return new_file_name(i + 1)
    else:
        return location

@app.route("/index")
def photo():
    return render_template('index.htm')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static/', filename)

@app.route('/receive_photo/', methods=['POST'])
def receive_photo():
    f = open(new_file_name(), 'wb')
    raw_data = request.form['img']
    cleaned_data = raw_data[raw_data.find(',')+1:]
    f.write(base64.decodestring(cleaned_data))
    f.close()
    return ''


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9001)
