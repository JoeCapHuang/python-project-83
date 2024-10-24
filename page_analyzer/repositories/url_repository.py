from datetime import datetime
from page_analyzer.tools import get_name_from_url


def add_url(conn, url):
    with conn.cursor() as cur:
        name = get_name_from_url(url)
        url_id = get_url_by_name(conn, name)

        if url_id:
            return url_id['id'], ('Страница уже существует', 'info')

        cur.execute("INSERT INTO urls (name, created_at)"
                    "VALUES (%s, %s) RETURNING id;", (name, datetime.now()))
        conn.commit()

        url_id = cur.fetchone()
        return url_id['id'], ('Страница успешно добавлена', 'success')


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
