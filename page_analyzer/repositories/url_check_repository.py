from datetime import datetime


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
