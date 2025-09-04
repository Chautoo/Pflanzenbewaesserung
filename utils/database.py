# db connection to read, update, delete
import traceback
from contextlib import contextmanager
from typing import Any, Dict, Iterable, List, Optional, Tuple

import pymysql
import pymysql.cursors


# Connection to database
def get_connection():
    host = "localhost"
    user = "root"
    password = "Kennwort*1"
    db = "Pflanzenbewaesserung"
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            charset='utf8mb4',  # Codepage UTF-8
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5,  # Try to connect for 5sec
            autocommit=False,
        )
        return conn

    except pymysql.MySQLError as e:
        err_type = type(e).__name__  # extract classname as str
        print(f"Can´t connect to database ({err_type}). Details:")
        print(f"- Host: {host}, User: {user}, DB: {db}")
        print(f"- Errorcode: {e}")
        traceback.print_exc()  # give full stacktrace in console
        raise  # trigger error again

    except Exception as e:
        print("Unknown Error while try to reach the database", type(e).__name__, e)
        traceback.print_exc()  # give full stacktrace in console
        raise

# makes sure that connections are opened and closed successfully
# contextmanager handels a 'with-block' to manage resources
@contextmanager
def connection():
    conn = None
    try:
        conn = get_connection()
        yield conn  # handles the connection
        conn.commit()  # automatically raise after 'with-block' finished
    # if an Error happened, reset connection
    except Exception:
        if conn is not None:
            try:
                conn.rollback()
            except Exception:
                pass
        raise
    # close programm
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass

# define set and get for table
def fetch_all(
        table: str,
        columns: Optional[Iterable[str]] = None,
        where: Optional[str] = None,
        params: Optional[Tuple[Any, ...]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None
) -> List[Dict[str, Any]]:

    cols = ", ".join(columns) if columns else "*"  # replace  cols with 'x' from row, if not set '*'
    sql = f"SELECT {cols} FROM {table}"  # get the cols from table 'table'

    if where:
        sql += f" WHERE {where}"
    if order_by:
        sql += f" ORDER BY {order_by}"
    if limit is not None:
        sql += f" LIMIT {int(limit)}"

    with connection() as conn:  # connect to db
        with conn.cursor() as cur:  # create cursor
            cur.execute(sql, params)  # execute different statement
            return list(cur.fetchall())

# return first row
def fetch_one(
        table: str,
        where: str,
        params: Tuple[Any, ...],  # placeholder for WHERE
        columns: Optional[Iterable[str]] = None  # list of column, if nothing in column replace with '*'
) -> Optional[Dict[str, Any]]:
    rows = fetch_all(
        table,
        columns=columns,
        where=where,
        params=params,
        limit=1  # set limit for output
    )
    return rows[0] if rows else None

# add somthing to a row
def insert_row(
        table: str,
        data: Dict[str, Any]
) -> int:
    keys = ", ".join(f"`{k}`" for k in data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    sql = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
    values = tuple(data.values())

    with connection() as conn:  # connect to db
        with conn.cursor() as cur:  # create courser
            cur.execute(sql, values)  # execute different statement
            return cur.lastrowid if hasattr(cur, "lastrowid") else 0

# update an existing row
def update_rows(
        table: str,
        data: Dict[str, Any],
        where: str,
        params: Tuple[Any, ...]
) -> int:
    set_clause = ", ".join(f"`{k}`=%s" for k in data.keys())
    sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
    values = tuple(data.values()) + params

    with connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, values)
            return cur.rowcount

# delete one row
def delete_rows(
        table: str,
        where: str,
        params:
        Tuple[Any, ...]
) -> int:
    sql = f"DELETE FROM {table} WHERE {where}"

    with connection() as conn:  # connect to db
        with conn.cursor() as cur:  # create cursor
            cur.execute(sql, params)  # execute different statement
            return cur.rowcount

# get from table
def get_messwerte_last(limit: int = 5) -> List[Dict[str, Any]]:
    return fetch_all("messwerte", order_by="ID DESC", limit=limit)

def get_pflanzen() -> List[Dict[str, Any]]:
    return fetch_all("pflanze", order_by="ID ASC")

# set for table
def set_pflanze_name(pflanzen_id: int, name: str) -> int:
    return update_rows("pflanze", {"Name": name}, "ID=%s", (pflanzen_id,))

def set_pflanze_schwellwert(pflanzen_id: int, schwellwert: Any) -> int:
    return update_rows("pflanze", {"Schwellwert": schwellwert}, "ID=%s", (pflanzen_id,))

# delete from table
def delete_pflanze(pflanzen_id: int) -> int:
    return delete_rows("pflanze", "ID=%s", (pflanzen_id,))

def delete_messwerte(messwerte_id: int) -> int:
    return delete_rows("messwerte", "ID=%s", (messwerte_id,))