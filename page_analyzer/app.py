from flask import Flask, render_template, flash
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def urls_index():
    return render_template('urls/index.html')


@app.route('/urls/<id>')
def url_show(id):
    return render_template('urls/show.html')
