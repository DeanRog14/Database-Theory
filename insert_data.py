import pymysql
import pandas as pd
import os

# Database connection details
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "my20@DEAN"
DB_NAME = "taxiData"

# File path for the dataset
FILE_PATH = "taxi-data-sorted-small.csv.bz2"

# Connect to MySQL database
connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
cursor = connection.cursor()

# Ensures that the file exists
if not os.path.exists(FILE_PATH):
    print(f"Error: File '{FILE_PATH}' not found!")
else:
    print(f"File '{FILE_PATH}' found successfully.")

# Trys to read the file and place them under these column names
try:
    columns = [
    "medallion", "hack_license", "pickup_datetime", "dropoff_datetime", "trip_time_in_secs", "trip_distance",
    "pickup_longitude", "pickup_latitude", "dropoff_longitude", "dropoff_latitude", "payment_type",
    "fare_amount", "surcharge", "mta_tax", "tip_amount", "tolls_amount", "total_amount"
    ]

    df = pd.read_csv(FILE_PATH, compression='bz2', names=columns, header=None)
    print("File read successfully!")
except Exception as e:
    print("Error reading file:", e)

# Clean up the data types
df['fare_amount'] = pd.to_numeric(df['fare_amount'], errors='coerce')
df['surcharge'] = pd.to_numeric(df['surcharge'], errors='coerce')
df['mta_tax'] = pd.to_numeric(df['mta_tax'], errors='coerce')
df['tip_amount'] = pd.to_numeric(df['tip_amount'], errors='coerce')
df['tolls_amount'] = pd.to_numeric(df['tolls_amount'], errors='coerce')
df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce')
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], errors='coerce')
df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'], errors='coerce')

df.dropna()



# SQL Insert query
insert_query = """
INSERT INTO TaxiTrips (medallion, hack_license, pickup_datetime, dropoff_datetime, trip_time_in_secs, trip_distance,
                      pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, payment_type,
                      fare_amount, surcharge, mta_tax, tip_amount, tolls_amount, total_amount)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Insert data row by row
print("Inserting data...")
data_to_insert = [
    (
        row.medallion, row.hack_license, row.pickup_datetime, row.dropoff_datetime,
        row.trip_time_in_secs, row.trip_distance, row.pickup_longitude, row.pickup_latitude,
        row.dropoff_longitude, row.dropoff_latitude, row.payment_type, row.fare_amount,
        row.surcharge, row.mta_tax, row.tip_amount, row.tolls_amount, row.total_amount
    )
    for row in df.itertuples(index=False)
]

cursor.executemany(insert_query, data_to_insert)

connection.commit()
cursor.close()
connection.close()
print("Data insertion completed.")
