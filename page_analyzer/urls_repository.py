import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse
from datetime import datetime


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


class URLRepository:

    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)

    def add_url(self, url):
        with self.conn.cursor() as cur:
            parsed_url = urlparse(url)
            name = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))

            cur.execute("SELECT id FROM urls WHERE name = %s;", (name,))
            url_id = cur.fetchone()

            if url_id:
                return url_id['id'], ('Страница уже существует', 'info')

            date = datetime.now().date()
            cur.execute("INSERT INTO urls (name, created_at)"
                        "VALUES (%s, %s) RETURNING id;", (name, date))
            self.conn.commit()

            url_id = cur.fetchone()
            return url_id['id'], ('Страница успешно добавлена', 'success')

    def get_all_urls(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM urls ORDER BY created_at DESC;")
            return cur.fetchall()

    def get_url_by_id(self, url_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s;", (url_id,))
            return cur.fetchone()

    def close(self):
        if self.conn:
            self.conn.close()
