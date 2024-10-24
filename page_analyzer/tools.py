import validators
from urllib.parse import urlparse, urlunparse


def get_name_from_url(url):
    parsed_url = urlparse(url)
    name = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))
    return name


def validate_url(url: str):

    if len(url) > 255:
        return False, ('URL превышает 255 символов', 'danger')

    if not url:
        return False, ('URL не может быть пустым', 'danger')

    if validators.url(url):
        return True, ('', '')

    return False, ('Некорректный URL', 'danger')
