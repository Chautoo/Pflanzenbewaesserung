# db connection


import sqlite3
import pymysql
import pymysql.cursors


# connect to database
try:
    connection = pymysql.connect(host="192.168.189.6",
                                 user="anakin",
                                 password="anakin2025!",
                                 db="flanzenbewaesserung",
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
except:
    print("Connection Error")

'''''
with connection:
    with connection.cursor() as cursor:
        sql = "INSERT INTO `role` (`id`, `name`, `type`, `value`) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)

    # commit to save changes
    connection.commit()

    with connection.cursor() as cursor:
        # read a single record
        sql = "SELECT * FROM `role`"
        cursor.execute(sql, (1, "test", "temperature", 20.0))
'''