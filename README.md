// Student names: Dean Roggenbauer and Matthew DeVaney 
// Student ID: 1305109 and 1306257

// Course number: 3337
// Course name: Database Theory and Applications
// Date Created: 1-31-2024

Programming Assignment 2

--------------------------------

create_database.sql 

CREATE DATABASE taxiData;

USE taxiData;

CREATE TABLE TaxiTrips (
    medallion VARCHAR(255),
    hack_license VARCHAR(255),
    pickup_datetime DATETIME,
    dropoff_datetime DATETIME,
    trip_time_in_secs INT,
    trip_distance FLOAT,
    pickup_longitude FLOAT,
    pickup_latitude FLOAT,
    dropoff_longitude FLOAT,
    dropoff_latitude FLOAT,
    payment_type VARCHAR(25),
    fare_amount FLOAT,
    surcharge FLOAT,
    mta_tax FLOAT,
    tip_amount FLOAT,
    tolls_amount FLOAT,
    total_amount FLOAT
);

--------------------------------
 
insert_data.py

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

    df = pd.read_csv(FILE_PATH, compression='bz2', names=columns)
    print("File read successfully!")
except Exception as e:
    print("Error reading file:", e)

# Clean up the data types to prepare for insertion
df['fare_amount'] = pd.to_numeric(df['fare_amount'], errors='coerce')
df['surcharge'] = pd.to_numeric(df['surcharge'], errors='coerce')
df['mta_tax'] = pd.to_numeric(df['mta_tax'], errors='coerce')
df['tip_amount'] = pd.to_numeric(df['tip_amount'], errors='coerce')
df['tolls_amount'] = pd.to_numeric(df['tolls_amount'], errors='coerce')
df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce')
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], errors='coerce')
df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'], errors='coerce')

# Drops any values that might be affecting data
df.dropna()

# Creates the SQL insert query with placeholders
insert_query = """
INSERT INTO TaxiTrips (medallion, hack_license, pickup_datetime, dropoff_datetime, trip_time_in_secs, trip_distance,
                      pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, payment_type,
                      fare_amount, surcharge, mta_tax, tip_amount, tolls_amount, total_amount)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Inserts the data row by row 
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
print("Data inserted successfully!")

--------------------------------

clean_and_query.sql

DELETE FROM taxitrips 
WHERE total_amount OR trip_distance = 0;

SELECT AVG(total_amount)
FROM taxitrips;

SELECT MAX(total_amount), MIN(total_amount)
FROM taxitrips;

SELECT hack_license, COUNT(*) AS rides
FROM taxitrips
GROUP BY hack_license
ORDER BY rides DESC
LIMIT 1;

SELECT payment_type, AVG(tip_amount)
FROM taxitrips
WHERE payment_type IN ('CSH', 'CRD')
GROUP BY payment_type;