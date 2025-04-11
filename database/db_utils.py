# db_utils.py
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def insert_weather(data):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO weather (city, timestamp, temperature, humidity, pressure, wind_speed)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (data['city'], data['timestamp'], data['temperature'], data['humidity'], data['pressure'], data['wind_speed']))
        conn.commit()

def insert_aqi(data):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO air_quality (city, timestamp, aqi, category)
                VALUES (%s, %s, %s, %s)
            """, (data['city'], data['timestamp'], data['aqi'], data['category']))
        conn.commit()
