# operations
from database import *


# get ony last 5 logs
def read_data():
    cursor.execute("SELECT * FROM messwerte ORDER BY ID DESC LIMIT 5")
    records = cursor.fetchone()
    for record in records:
        print(record[0])

# get the average of the last 5
def print_average_last5(column):
    try:
        avg = read_data()
        if avg is None:
            print("No data available")
        else:
            avg = avg[column]
            avg = avg.mean()
            print(avg)

    except Exception as e:
        print("Something went Wrong", e)
