from contextlib import contextmanager
import sqlite3


@contextmanager
def get_db_connection(db_name='dados.db'):
    conn = sqlite3.connect(db_name)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()