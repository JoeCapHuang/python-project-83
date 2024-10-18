from flask import Flask, render_template, flash, request, redirect, url_for
import validators
import os
from dotenv import load_dotenv
from .url_repositories import URLRepository


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET'])
def urls_index():
    repo = URLRepository()
    all_urls = repo.get_all_urls()
    repo.close()
    return render_template('urls/index.html', urls=all_urls)


@app.route('/urls', methods=['POST'])
def urls_post():
    url = request.form.get('url')

    if len(url) > 255:
        flash('URL превышает 255 символов', 'danger')
        return redirect(url_for('index'))

    if not url:
        flash('URL не может быть пустым', 'danger')
        return redirect(url_for('index'))

    if validators.url(url):
        repo = URLRepository()
        repo_id, message = repo.add_url(url)
        repo.close()
        flash(*message)
        return redirect(url_for('url_show', url_id=repo_id))

    else:
        flash('Некорректный URL', 'danger')
        return redirect(url_for('index'))


@app.route('/urls/<url_id>')
def url_show(url_id):
    repo = URLRepository()
    url_data = repo.get_url_by_id(url_id)
    checks = repo.get_all_checks(url_id)
    repo.close()

    return render_template('urls/show.html', url=url_data, checks=checks)


@app.route('/urls/<url_id>/checks', methods=['POST'])
def checks_post(url_id):
    repo = URLRepository()
    check = {}
    repo.add_check(url_id, check)
    repo.close()
    flash('Страница успешно проверена', 'success')
    return redirect((url_for('url_show', url_id=url_id)))
