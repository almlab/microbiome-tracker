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

@app.route("/")
def root():
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
