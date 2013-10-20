import os
import sys
import base64
import datetime
path = os.path.dirname(os.path.realpath(__file__))+'/photos/'
sys.path.append(path)


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
    location = 'static/photos/'+str(i)+'.jpg'
    if os.path.exists(location):
        return new_file_name(i + 1)
    else:
        return location


# Default page that allows user to take pictures and upload them
@app.route("/index")
def photo():
    #if 'username' not in session:
    #    return redirect(url_for('login'))
    return render_template('index.htm')

# Utility page to load static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static/', filename)

# Page for server to receive photos
@app.route('/receive_photo/', methods=['POST'])
def receive_photo():
    #if 'username' not in session:
    #    return redirect(url_for('login'))
    # user = session['username']

    # Save photo
    file_location = new_file_name()
    f = open(file_location, 'wb')
    raw_data = request.form['img']
    cleaned_data = raw_data[raw_data.find(',')+1:]
    f.write(base64.decodestring(cleaned_data))
    f.close()

    # TODO - Make this save to the database
    file_location
    #user
    timestamp = datetime.datetime.now()

    return ''

# Page for users to annotate photos
@app.route('/annotate/', methods=['GET'])
def annotate_photo():
    #if 'username' not in session:
    #    return redirect(url_for('login'))
    # TODO - Make this read from the database
    img_id = 1
    img_src = '/static/photos/1.jpg'
    timestamp = 'October 19, 2013'

    # TODO - Make this read usernames from the session
    #user = session['username']
    user = 'Fake User'

    kwargs = {}
    kwargs['img_id'] = img_id
    kwargs['img_src'] = img_src
    kwargs['user'] = user
    kwargs['timestamp'] = timestamp
    return render_template('annotate.htm', **kwargs)

@app.route('/annotate/', methods=['POST'])
def save_annotation():
    #if 'username' not in session:
    #    return redirect(url_for('login'))
    img_id = request.form['img_id']
    annotation = request.form['annotation']
    annotator = session['username']
    # TODO - Make this save to the database

    return redirect(url_for('annotate_photo'))

# Page for users to see their history
@app.route('/history/')
def history():
    #if 'username' not in session:
    #    return redirect(url_for('login'))
    return render_template('history.htm')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9001)
