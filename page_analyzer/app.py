from flask import Flask, render_template, flash, request, redirect, url_for
import validators
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET'])
def urls_index():
    return render_template('urls/index.html')


@app.route('/urls', methods=['POST'])
def urls_post():
    url = request.form.get('url')
    if not url:
        flash('URL не может быть пустым', 'error')

    if validators.url(url):
        
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('urls_index'))

    else:
        flash('Некорректный URL', 'error')
        return redirect(url_for('index'))


@app.route('/urls/<id>')
def url_show(id):
    return render_template('urls/show.html')
