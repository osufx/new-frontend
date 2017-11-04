import datetime
import json

from flask import Flask, make_response, redirect, request, render_template, url_for, flash

from helpers import mysql, hash, checks, recaptcha

with open("config.json", "r") as f:
    config = json.load(f)

with open("recaptcha.json", "r") as f:
    rconfig = json.load(f)

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
    '''
    TODO:
    Add regex to username check - (?=^.{3,20}$)^[a-zA-Z][a-zA-Z0-9]*[._-]?[a-zA-Z0-9]+$
    Add regex to password check - ^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*_=+-]).{8,12}$
    Add regex to email check - [^@]+@[^@]+\.[a-zA-Z]{2,}
    '''
    logged_in = checks.is_logged_in(request)

    if logged_in:
        return redirect(url_for('home'))

    if request.method == 'POST':

        if not recaptcha.verify(request):
            flash('Captcha error!')

        else:
            username = request.form['username']
            email = request.form['email']

            if checks.does_user_exist(username=username):
                flash('Username exist!')
            elif checks.does_user_exist(email=email):
                flash('Email is used by other user!')

            else:
                password = hash.password(request.form['password'])

                if password != hash.password(request.form['rpassword']):
                    flash('Passwords do not match!')

                else:
                    connection, cursor = mysql.connect()
                    mysql.execute(connection, cursor,
                                  "INSERT INTO `users` (`username`, `password`, `email`) VALUES (%s, %s, %s)",
                                  [username, password, email])
                    flash('Your account is created, please login.')
                    return redirect(url_for('home'))

    return render_template('register.html', logged_in=logged_in)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username != "" and password != "":

            hashed_password = hash.password(password)

            if checks.does_user_exist(username):

                connection, cursor = mysql.connect()
                check_password = mysql.execute(connection, cursor,
                                               "SELECT password FROM users WHERE username = %s",
                                               [username]).fetchone()

                if check_password["password"] == hashed_password:

                    expire_date = datetime.datetime.now()
                    expire_date = expire_date + datetime.timedelta(days=90)

                    response = make_response(redirect('/'))
                    response.set_cookie('username', username, expires=expire_date)
                    response.set_cookie('password', hashed_password, expires=expire_date)
                    flash('You login successfully.')

                    return response

                else:

                    flash('Wrong password')

            else:

                flash('Wrong username')

        else:

            flash('Please fill the form')

    return redirect(url_for('home'))


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':

        if checks.is_logged_in(request):

            red = make_response(redirect(url_for('home')))
            red.set_cookie('username', '', expires=0)
            red.set_cookie('password', '', expires=0)
            flash('You logout successfully.')
            return red

        else:

            return redirect(url_for('home'))

    return redirect(url_for('home'))


@app.errorhandler(404)
def not_found(error):
    return 'This is error page...'


if __name__ == "__main__":
    app.run(**config)
