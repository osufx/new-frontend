from flask import Flask, make_response, redirect, request, render_template, url_for
import json
import datetime
from helpers import mysql, hash, checks

with open("config.json", "r") as f:
    config = json.load(f)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():

    logged_in = checks.is_logged_in(request)

    return render_template('index.html', logged_in=logged_in)

@app.route('/download/', methods=['GET', 'POST'])
def download():

    logged_in = checks.is_logged_in(request)

    return render_template('download.html', logged_in=logged_in)


@app.route('/faq/', methods=['GET', 'POST'])
def faq():

    logged_in = checks.is_logged_in(request)

    return render_template('faq.html', logged_in=logged_in)


@app.route('/help/', methods=['GET', 'POST'])
def help():

    logged_in = checks.is_logged_in(request)

    return render_template('help.html', logged_in=logged_in)

@app.route('/register/', methods=['GET', 'POST'])
def register():

    logged_in = checks.is_logged_in(request)

    return render_template('register.html', logged_in=logged_in)

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

    return redirect(url_for('home'))

@app.route('/logout/', methods=['GET', 'POST'])
def logout():

    if request.method == 'POST':

        if checks.is_logged_in(request):

            red = make_response(redirect(url_for('home')))
            red.set_cookie('username', '', expires=0)
            red.set_cookie('password', '', expires=0)

            return red

        else:

            return redirect(url_for('home'))

    return redirect(url_for('home'))

@app.errorhandler(404)
def not_found(error):

    return 'This is error page...'

if __name__ == "__main__":

    app.run(**config)