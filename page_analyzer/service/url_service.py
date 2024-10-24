import requests
from ..repositories.url_check_repository import add_check, get_all_checks
from ..repositories.url_repository import (
    add_url,
    get_all_urls,
    get_url_by_id
)
from page_analyzer.db.database import DatabaseConnection


def create_url(url):
    with DatabaseConnection() as conn:
        return add_url(conn, url)


def list_urls():
    with DatabaseConnection() as conn:
        return get_all_urls(conn)


def get_url_details(url_id):
    with DatabaseConnection() as conn:
        url_data = get_url_by_id(conn, url_id)
        checks = get_all_checks(conn, url_id)
    return url_data, checks


def perform_url_check(url_id):
    try:
        with DatabaseConnection() as conn:
            url_data = get_url_by_id(conn, url_id)
            url = url_data.get('name')
            response = requests.get(url, timeout=1)
            response.raise_for_status()

            check_data = {
                'status_code': response.status_code,
                'h1': '',
                'title': '',
                'description': ''
            }
            add_check(conn, url_id, check_data)
            return 'Страница успешно проверена', 'success'

    except requests.exceptions.RequestException:
        return 'Произошла ошибка при проверке', 'danger'
