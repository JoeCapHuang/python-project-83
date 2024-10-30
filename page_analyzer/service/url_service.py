import requests
from page_analyzer.repositories.url_check_repository import add_check, get_all_checks
from page_analyzer.repositories.url_repository import get_url_by_id
from bs4 import BeautifulSoup


def get_url_details(conn, url_id):
    url_data = get_url_by_id(conn, url_id)
    checks = get_all_checks(conn, url_id)
    return url_data, checks


def perform_url_check(conn, url_id):
    try:
        url_data = get_url_by_id(conn, url_id)
        url = url_data.get('name')
        check_data = fetch_and_parse_url(url)
        add_check(conn, url_id, check_data)
        return 'Страница успешно проверена', 'success'

    except requests.exceptions.RequestException:
        return 'Произошла ошибка при проверке', 'danger'


def fetch_and_parse_url(url):
    try:
        response = requests.get(url, timeout=1)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        h1 = soup.h1.string if soup.h1 else ''
        title = soup.title.string if soup.title else ''
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        description = desc_tag.get('content', '') if desc_tag else ''

        check_data = {
            'status_code': response.status_code,
            'h1': h1,
            'title': title,
            'description': description
        }
        return check_data

    except requests.exceptions.RequestException as e:
        raise e
