# db connection
import sys
import traceback

import pymysql
import pymysql.cursors


# connection to db
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
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5,
        )
        return conn

    except pymysql.MySQLError as e:
        err_type = type(e).__name__
        print(f"Can´t connect to database ({err_type}). Details:")
        print(f"- Host: {host}, User: {user}, DB: {db}")
        print(f"- Errorcode: {e}")
        traceback.print_exc()
        raise

    except Exception as e:
        print("Unknown Error while try to reach the database", type(e).__name__, e)
        traceback.print_exc()
        raise

auth = None
try:
    auth = get_connection()
except Exception as e:
    print("Auth was not successful.", type(e).__name__, e)
    sys.exit(1)

# read from a database "messwerte"
sql_messwerte = "SELECT * FROM messwerte"

try:
    with auth.cursor() as cursor:
        cursor.execute(sql_messwerte)
        result = cursor.fetchall()

        for record in result:
            ID = record.get("ID")
            PID = record.get("PID")
            Zeit = record.get("Zeit")
            Humidity = record.get("Humidity")
            Light = record.get("Light")
            Temperature = record.get("Temperature")
            Air = record.get("Air")
            print(ID, PID, Zeit, Humidity, Light, Temperature, Air)

except pymysql.MySQLError as e:
    print("SQL-Error while reading 'messwerte':", e)
    traceback.print_exc()

except Exception as e:
    print("Unexpected Error happened 'messwerte':", type(e).__name__, e)
    traceback.print_exc()


# read from a database "pflanze"
sql_pflanze = "SELECT * FROM pflanze"

try:
    with auth.cursor() as cursor:
        cursor.execute(sql_pflanze)
        result = cursor.fetchall()
        for record in result:
            ID = record.get("ID")
            Schwellwert = record.get("Schwellwert")
            Name = record.get("Name")
            print(ID, Schwellwert, Name)

except pymysql.MySQLError as e:
    print("SQL-Error while reading 'pflanze':", e)
    traceback.print_exc()
except Exception as e:
    print("Unexpected Error happened 'pflanze':", type(e).__name__, e)
    traceback.print_exc()

finally:
    if auth is not None:
        try:
            auth.close()
        except Exception:
            pass