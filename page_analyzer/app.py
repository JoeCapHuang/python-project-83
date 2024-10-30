from flask import Flask, render_template, flash, request, redirect, url_for
from dotenv import load_dotenv
from page_analyzer.db.database import DatabaseConnection
from page_analyzer.repositories.url_repository import get_all_urls, add_url
from page_analyzer.tools import validate_url
from page_analyzer.service.url_service import (
    get_url_details,
    perform_url_check
)
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET'])
def urls_index():
    with DatabaseConnection(DATABASE_URL) as conn:
        urls = get_all_urls(conn)
    return render_template('urls/index.html', urls=urls)


@app.route('/urls', methods=['POST'])
def urls_post():
    url = request.form.get('url')
    validity, message = validate_url(url)
    if not validity:
        flash(*message)
        return render_template('index.html'), 422
    with DatabaseConnection(DATABASE_URL) as conn:
        url_id, message = add_url(conn, url)
    flash(*message)
    return redirect(url_for('url_show', url_id=url_id))


@app.route('/urls/<url_id>')
def url_show(url_id):
    with DatabaseConnection(DATABASE_URL) as conn:
        url_data, checks = get_url_details(conn, url_id)
    return render_template('urls/show.html', url=url_data, checks=checks)


@app.route('/urls/<url_id>/checks', methods=['POST'])
def checks_post(url_id):
    with DatabaseConnection(DATABASE_URL) as conn:
        message = perform_url_check(conn, url_id)
    flash(*message)
    return redirect(url_for('url_show', url_id=url_id))
