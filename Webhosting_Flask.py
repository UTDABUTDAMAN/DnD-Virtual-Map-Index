

from flask import Flask, request,render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Wickermoor_Village_Map')
def Wickermoor_Village_Map():
    return render_template('Wickermoor_Village_Map.html')

