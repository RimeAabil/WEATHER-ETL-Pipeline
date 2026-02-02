import os
from api import fetch_data, fetch_mock_data
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[2] / ".env"

load_dotenv(env_path)

# Use POSTGRES_* env vars (provide sensible defaults)
db_host = os.getenv("DB_HOST", "postgres")
db_name = os.getenv("POSTGRES_DB", "weather_db")
db_user = os.getenv("POSTGRES_USER", "db_user")
db_password = os.getenv("POSTGRES_PASSWORD", "db_password")


def connect_to_db(HOST=db_host, DB=db_name, USER=db_user, PASSWORD=db_password):
    try:
        conn = psycopg2.connect(
            host=HOST,
            port=5432,
            database=DB,
            user=USER,
            password=PASSWORD
        )
        print("Connected successfully!")
        return conn
    except Exception as e:
        print("An error occurred while connecting to the database:", e)
        return None
    

def create_table(conn):
    if conn is None:
        raise RuntimeError("Database connection is not established.")

    print("Creating weather table if not exits ...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data(
                       id SERIAL PRIMARY KEY,
                       city TEXT,
                       temperature FLOAT,
                       weather_descriptions TEXT,
                       wind_speed FLOAT,
                       time TIMESTAMP,
                       inserted_at TIMESTAMP DEFAULT NOW(),
                       utc_offset TEXT);
        """)

        conn.commit()
        print("Table created successfully!")
    except psycopg2.Error as e:
        print(f"An error occurred while creating the table: {e}")


def insert_record(conn, data):
    print("Inserting weather data into the database...")
    try:
       
       weather = data["current"]
       location = data["location"]

       cursor = conn.cursor() 
       cursor.execute("""
                    INSERT INTO dev.raw_weather_data (
                       city,
                       temperature,
                       weather_descriptions,
                       wind_speed,
                       time,
                       inserted_at,
                       utc_offset)
                       VALUES (%s, %s,%s, %s, %s, NOW(), %s)

        """, (location["name"], 
              weather["temperature"],
              weather["weather_descriptions"][0],
              weather["wind_speed"],
              location["localtime"],
              location["utc_offset"]    
        ))
       conn.commit()
       print("Data inserted successfully!")
    except psycopg2.Error as e:
        print(f"An error occurred while inserting data: {e}")
        raise


def main():
    try:
        conn = connect_to_db()
        create_table(conn)
        # Use real data from API
        data = fetch_data()
        if data:
            insert_record(conn, data)
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()