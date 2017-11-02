from flask import Flask, make_response, redirect, request, render_template, url_for
import json
from helpers import mysql

with open("config.json", "r") as f:
    config = json.load(f)

app = Flask(__name__)
#app.secret_key = config["secret_key"]

@app.route('/')
def home():

    return render_template('index.html')

@app.route('/download/')
def download():

    return render_template('download.html')


@app.route('/faq/')
def faq():

    return render_template('faq.html')


@app.route('/help/')
def help():

    return render_template('help.html')

@app.route('/register/')
def register():

    return render_template('register.html')

if __name__ == "__main__":

    app.run(**config)