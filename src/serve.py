import json
import os
import sys
import base64
path = os.path.dirname(os.path.realpath(__file__))+'/photos/'
sys.path.append(path)

from flask import Flask, render_template, request
app = Flask(__name__)

def new_file_name(i = 0):
    location = 'photos/'+str(i)+'.jpg'
    if os.path.exists(location):
        return new_file_name(i + 1)
    else:
        return location

# Default page that allows user to take pictures and upload them
@app.route("/")
def root():
    return render_template('index.htm')

# Utility page to load static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static/', filename)

# Page for server to receive photos
@app.route('/receive_photo/', methods=['POST'])
def receive_photo():
    f = open(new_file_name(), 'wb')
    raw_data = request.form['img']
    cleaned_data = raw_data[raw_data.find(',')+1:]
    f.write(base64.decodestring(cleaned_data))
    f.close()
    return ''

# Page for users to annotate photos
@app.route('/annotate/')
def annotate_photo():
    img_src = '/static/photos/1.jpg'
    return render_template('annotate.htm', img_src=img_src)

# Page for users to see their history
@app.route('/history/')
def history():
    return ''


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9001)
