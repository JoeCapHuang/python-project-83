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

            date = datetime.now()
            cur.execute("INSERT INTO urls (name, created_at)"
                        "VALUES (%s, %s) RETURNING id;", (name, date))
            self.conn.commit()

            url_id = cur.fetchone()
            return url_id['id'], ('Страница успешно добавлена', 'success')

    def get_all_urls(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    urls.id,
                    urls.name,
                    url_checks.status_code AS last_status_code,
                    url_checks.created_at AS last_check_date
                FROM
                    urls
                LEFT JOIN (
                    SELECT DISTINCT ON (url_id) *
                    FROM url_checks
                    ORDER BY url_id, created_at DESC
                ) AS url_checks ON urls.id = url_checks.url_id
                ORDER BY urls.id;
            """)
            return cur.fetchall()

    def get_url_by_id(self, url_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s;", (url_id,))
            return cur.fetchone()

    def close(self):
        if self.conn:
            self.conn.close()


class URLCheckRepository:

    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)

    def add_check(self, url_id, check: dict):
        status_code = check.get('status_code')
        h1 = check.get('h1')
        title = check.get('title')
        description = check.get('description')
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO url_checks
                (url_id, status_code, h1, title, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    url_id,
                    status_code,
                    h1,
                    title,
                    description,
                    datetime.now()
                )
            )
            self.conn.commit()
            check_id = cur.fetchone()
            return check_id

    def get_all_checks(self, url_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM url_checks "
                        "WHERE url_id = %s "
                        "ORDER BY created_at DESC;", (url_id,))
            return cur.fetchall() or []

    def close(self):
        if self.conn:
            self.conn.close()
