import os
import base64

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE='db/database.sqlite',
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

## --- database-related stuff ---
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    """Creates the database tables."""
    with app.app_context():
        new_db = False
        if not os.path.exists(app.config['DATABASE']):
            new_db = True
        db = get_db()
        if new_db:
            with app.open_resource('db/schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
## ---

def new_file_name(i = 0):
    location = 'static/photos/'+str(i)+'.jpg'
    if os.path.exists(location):
        return new_file_name(i + 1)
    else:
        return location

# Utility page to load static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static/', filename)


# Login page
@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')

# Check login
@app.route('/', methods=['POST'])
def do_login():
    db = get_db()
    username = request.form['username']
    password = request.form['password']
    credentials = db.execute('SELECT id_person FROM person WHERE username=? AND password=?', [username, password]).fetchone()
    if credentials == None:
        flash("Invalid Log In")
        return render_template('login.html')
    else:
        session['logged_in'] = True
        session['username'] = username
        session['user_id'] = credentials[0]
        return redirect(url_for('record'))

# Logout Page
@app.route('/logout')
def logout():
    if 'username' not in session:
        return redirect(url_for('login'))
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('login'))
	

# Page for registration
@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def do_register():
    db = get_db()
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password2']
    if password != password2:
        flash('Error - passwords did not match!')
        return render_template('register.html')
    else:
        db.execute('INSERT INTO person (username, password) VALUES (?, ?)', (username, password))
        db.commit()
        return render_template('login.html')

# Default page that allows user to take pictures and upload them
@app.route("/record")
def record():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('record.htm')

# Page for server to receive photos
@app.route('/receive_photo/', methods=['POST'])
def receive_photo():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Save photo
    file_location = new_file_name()
    f = open(file_location, 'wb')
    raw_data = request.form['img']
    cleaned_data = raw_data[raw_data.find(',')+1:]
    f.write(base64.decodestring(cleaned_data))
    f.close()

    user_id = session['user_id']
    db = get_db()
    db.execute('INSERT INTO food (file_location, trackperson, annotation) VALUES (?, ?, ?)',
                [file_location, user_id, ''])
    db.commit()
    return ''

# Page for users to annotate photos
@app.route('/annotate/', methods=['GET'])
def annotate():
    if 'username' not in session:
        return redirect(url_for('login'))
    id_food = request.args.get('id_food')
    db = get_db()
    if id_food == None:
        food = db.execute('SELECT * FROM food WHERE annotation="" AND trackperson=? ORDER BY id_food DESC LIMIT 1', [session['user_id']]).fetchone()
    else:
        food = db.execute('SELECT * FROM food WHERE id_food=? AND trackperson=? ORDER BY id_food DESC LIMIT 1', [id_food, session['user_id']]).fetchone()
    if food == None:
        return render_template('annotate.htm', no_pictures=True)
    food = dict(food)
    food['user'] = session['username']
    return render_template('annotate.htm', **food)

# Page To Save annotations
@app.route('/annotate/', methods=['POST'])
def save_annotation():
    if 'username' not in session:
        return redirect(url_for('login'))
    id_food = request.form['id_food']
    annotation = request.form['annotation']
    db = get_db()
    db.execute('UPDATE food SET annotation=? WHERE id_food=?',
                 [annotation, id_food])
    db.commit()
    return redirect(url_for('annotate'))

@app.route("/wellness", methods=['GET'])
def wellness():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('wellness.htm')

@app.route("/wellness", methods=['POST'])
def add_wellness():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('add_wellness'))



# Page for users to see their history
@app.route('/history/')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))
    db = get_db()
    cur = db.execute('SELECT * FROM food ORDER BY id_food')
    entries = cur.fetchall()
    return render_template('history.htm', entries=entries)


@app.route("/delete/")
def delete():
    if 'username' not in session:
        return redirect(url_for('login'))
    id_food = request.args.get('id_food')
    user_id = session['user_id']
    db = get_db()
    db.execute('DELETE FROM food WHERE id_food=? AND trackperson=?', [id_food, user_id])
    db.commit()
    return redirect(url_for('history'))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host='0.0.0.0', port=9001)
