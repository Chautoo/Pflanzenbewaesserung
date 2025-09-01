# db connection

import pymysql.cursors


# connect to database
try:
    auth = pymysql.connect(host="192.168.189.6",
                           user="anakin",
                           password="anakin2025!",
                           db="flanzenbewaesserung",
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
except:
    print('Can´t connect to database', auth)

# create cursor
cursor = auth.cursor()

# read from a database "messwerte"
sql_query = ("SELECT * FROM messwerte")

# execute the query
try:
    cursor.execute(sql_query)
    result = cursor.fetchall()

    for record in result:
        ID = record[0]
        PID = record[1]
        Zeit = record[2]
        Humidity = record[3]
        Light = record[4]
        Temperature = record[5]
        Air = record[6]

        print(ID, PID, Zeit, Humidity, Light, Temperature, Air)

except Exception as e:
    print("Exception Occurred", e)

cursor.close()

# read from a database "pflanze"
sql_query = ("SELECT * FROM pflanze")

# execute the query
try:
    cursor.execute(sql_query)
    result = cursor.fetchall()

    for record in result:
        ID = record[0]
        Schwellwert = record[1]
        Name = record[2]

        print(ID, Schwellwert, Name)

except Exception as e:
    print("Exception Occurred", e)

cursor.close()