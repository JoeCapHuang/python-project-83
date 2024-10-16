from flask import Flask, render_template, flash, request, redirect, url_for
import validators
import os
from dotenv import load_dotenv
from .urls_repository import URLRepository


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
        flash('URL не должен превышать 255 символов', 'error')
        return redirect(url_for('index'))

    if not url:
        flash('URL не может быть пустым', 'error')
        return redirect(url_for('index'))

    if validators.url(url):
        repo = URLRepository()
        repo_id, message = repo.add_url(url)
        repo.close()
        flash(*message)
        return redirect(url_for('url_show', url_id=repo_id))

    else:
        flash('Некорректный URL', 'error')
        return redirect(url_for('index'))


@app.route('/urls/<url_id>')
def url_show(url_id):
    repo = URLRepository()
    url_data = repo.get_url_by_id(url_id)
    repo.close()

    return render_template('urls/show.html', url=url_data)
