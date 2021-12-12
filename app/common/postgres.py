import psycopg2
from .settings import POSTGRES


class _DB:
    def __init__(self):
        self._connect()

    def _connect(self):
        self.conn = psycopg2.connect(**POSTGRES)
        self.cur = self.conn.cursor()
        self.conn.autocommit = True


_db = _DB()
