import json
import os
import sys
path = os.path.dirname(os.path.realpath(__file__))+'/photos/'
sys.path.append(path)

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index.htm')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static/', filename)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9001)
