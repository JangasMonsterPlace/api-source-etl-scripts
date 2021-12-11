import psycopg2
from .settings import POSTGRES
from sqlalchemy import create_engine

class _DB:
    def __init__(self):
        pass
        # self._connect()

    def _connect(self):
        self.conn = psycopg2.connect(**POSTGRES)
        self.cur = self.conn.cursor()
        self.conn.autocommit = True

    def _engine(self):
        
        return create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'.format(**POSTGRES))




_db = _DB()
