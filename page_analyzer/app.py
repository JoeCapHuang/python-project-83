import os
from dotenv import load_dotenv
import requests
from flask import (
    Flask,
    render_template,
    flash,
    request,
    redirect,
    url_for
)
from page_analyzer.db import (
    DatabaseConnection,
    add_check,
    get_url_by_id,
    get_all_checks,
    get_all_urls,
    add_url,
)
from page_analyzer.utils import validate_url, fetch_and_parse_url, get_base_url

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
        base_url = get_base_url(url)
        url_id, was_created = add_url(conn, base_url)
        if not was_created:
            flash('Страница уже существует', 'info')
        else:
            flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_show', url_id=url_id))


@app.route('/urls/<url_id>')
def url_show(url_id):
    with DatabaseConnection(DATABASE_URL) as conn:
        url_data = get_url_by_id(conn, url_id)
        checks = get_all_checks(conn, url_id)
    return render_template('urls/show.html', url=url_data, checks=checks)


@app.route('/urls/<url_id>/checks', methods=['POST'])
def checks_post(url_id):
    try:
        with DatabaseConnection(DATABASE_URL) as conn:
            url_data = get_url_by_id(conn, url_id)
            url = url_data.get('name')
            check_data = fetch_and_parse_url(url)
            add_check(conn, url_id, check_data)
        flash('Страница успешно проверена', 'success')
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('url_show', url_id=url_id))
