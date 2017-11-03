from flask import Flask, make_response, redirect, request, render_template, url_for
import json
import hashlib
import datetime
from helpers import mysql, hash, checks

with open("config.json", "r") as f:
    config = json.load(f)

app = Flask(__name__)
#app.secret_key = config["secret_key"]

@app.route('/', methods=['GET', 'POST'])
def home():

    logged_in = checks.is_logged_in(request)

    return render_template('index.html', logged_in=logged_in)

@app.route('/download/', methods=['GET', 'POST'])
def download():

    return render_template('download.html')


@app.route('/faq/', methods=['GET', 'POST'])
def faq():

    return render_template('faq.html')


@app.route('/help/', methods=['GET', 'POST'])
def help():

    return render_template('help.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():

    return render_template('register.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username != "" and password != "":

            hashed_password = hash.password(password)

            expire_date = datetime.datetime.now()
            expire_date = expire_date + datetime.timedelta(days=90)

            response = make_response(redirect('/'))
            response.set_cookie('username', username, expires=expire_date)
            response.set_cookie('password', hashed_password, expires=expire_date)

            return response

    return 'ERROR'

if __name__ == "__main__":

    app.run(**config)