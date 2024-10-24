from flask import Flask, render_template, flash, request, redirect, url_for
from dotenv import load_dotenv
from .tools import validate_url
from .service.url_service import (
    create_url,
    list_urls,
    get_url_details,
    perform_url_check
)
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET'])
def urls_index():
    urls = list_urls()
    return render_template('urls/index.html', urls=urls)


@app.route('/urls', methods=['POST'])
def urls_post():
    url = request.form.get('url')
    validity, message = validate_url(url)
    if not validity:
        flash(*message)
        return redirect(url_for('index'))

    url_id, message = create_url(url)
    flash(*message)
    return redirect(url_for('url_show', url_id=url_id))


@app.route('/urls/<url_id>')
def url_show(url_id):
    url_data, checks = get_url_details(url_id)
    return render_template('urls/show.html', url=url_data, checks=checks)


@app.route('/urls/<url_id>/checks', methods=['POST'])
def checks_post(url_id):
    message = perform_url_check(url_id)
    flash(*message)
    return redirect(url_for('url_show', url_id=url_id))
