import validators
from urllib.parse import urlparse, urlunparse
import requests
from bs4 import BeautifulSoup


def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))
    return base_url


def validate_url(url: str):

    if len(url) > 255:
        return False, ('URL превышает 255 символов', 'danger')

    if not url:
        return False, ('URL не может быть пустым', 'danger')

    if validators.url(url):
        return True, ('', '')

    return False, ('Некорректный URL', 'danger')


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
