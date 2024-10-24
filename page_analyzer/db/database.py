import psycopg2
from psycopg2.extras import DictCursor
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


class DatabaseConnection:
    def __enter__(self):
        self.conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
