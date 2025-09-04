# operations
from database import get_messwerte_last


# get only last 5 logs
def read_data():
    records = get_messwerte_last(5)
    for record in records:
        print(record)
    return records

# get average of the last 5 for a column like 'Humidity'
def average_last5(column):
    try:
        records = read_data()  # read data
        if not records:
            print("No data available")  # if no data where given
        # if data available get only int and float
        values = [r.get(column) for r in records if isinstance(r.get(column), (int, float))]
        if not values:
            print(f"No numeric values for column '{column}' in the last 5 records")
        # take values and get average of them
        avg = sum(values) / len(values)
        print(avg)
    except Exception as e:
        print("Something went Wrong", e)

print(average_last5(column="Air"))