from typing import List, Tuple
from psycopg2.extras import execute_values
from .domain_types import TransformedTextData
from .postgres import _db


class ORM:
    @staticmethod
    def insert_transformed_review_data(data: List[Tuple]):
        sql = f"""
            INSERT INTO texts ({','.join(TransformedTextData.__annotations__.keys())})  VALUES %s
            ON CONFLICT (id) DO NOTHING
        """
        execute_values(_db.cur, sql, data)
