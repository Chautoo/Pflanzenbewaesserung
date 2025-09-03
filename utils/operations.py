# Utility operations
import sys
from logging import exception

import database


def get_log(air_value=None):
    conn = None
    try:
        conn = database.get_connection()
        with conn.cursor() as cursor:
            if air_value is None:
                cursor.execute("SELECT * FROM messwerte ORDER BY ID DESC LIMIT 5")
            else:
                cursor.execute("SELECT * FROM messwerte WHERE Air=%s ORDER BY ID DESC LIMIT 5", (air_value,))
            return cursor.fetchone()
    finally:
        if conn is not None:
            conn.close()
        exception(msg="No database connection")
