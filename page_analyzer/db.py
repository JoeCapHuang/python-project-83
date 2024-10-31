import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime


class DatabaseConnection:
    def __init__(self, database_url):
        self.database_url = database_url

    def __enter__(self):
        self.conn = psycopg2.connect(self.database_url, cursor_factory=DictCursor)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


def add_url(conn, name) -> tuple[int, bool]:
    url_id = get_url_by_name(conn, name)

    if url_id:
        return url_id['id'], False

    with conn.cursor() as cur:
        cur.execute("INSERT INTO urls (name, created_at)"
                    "VALUES (%s, %s) RETURNING id;", (name, datetime.now()))
        conn.commit()
        url_id = cur.fetchone()
        return url_id['id'], True


def get_all_urls(conn):
    with conn.cursor() as cur:
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


def get_url_by_name(conn, name):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM urls WHERE name = %s;", (name,))
        return cur.fetchone()


def get_url_by_id(conn, url_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM urls WHERE id = %s;", (url_id,))
        return cur.fetchone()


def add_check(conn, url_id, check_data: dict):
    status_code = check_data.get('status_code')
    h1 = check_data.get('h1')
    title = check_data.get('title')
    description = check_data.get('description')
    with conn.cursor() as cur:
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
        conn.commit()
        check_id = cur.fetchone()
        return check_id


def get_all_checks(conn, url_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM url_checks "
                    "WHERE url_id = %s "
                    "ORDER BY created_at DESC;", (url_id,))
        return cur.fetchall() or []
