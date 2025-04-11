# api/main.py

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from dotenv import load_dotenv
import os
from typing import List
from datetime import datetime, timedelta
from api.models import WeatherReading, AQIRecord

load_dotenv()

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

@app.get("/")
def root():
    return {"message": "AtmosStream API is running"}

@app.get("/weather/latest", response_model=WeatherReading)
def get_latest_weather(city: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT city, timestamp, temperature, humidity, pressure, wind_speed
                FROM weather
                WHERE city = %s
                ORDER BY timestamp DESC
                LIMIT 1
            """, (city,))
            row = cur.fetchone()
    return WeatherReading(
        city=row[0], timestamp=row[1], temperature=row[2],
        humidity=row[3], pressure=row[4], wind_speed=row[5]
    )

@app.get("/aqi/latest", response_model=AQIRecord)
def get_latest_aqi(city: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT city, timestamp, aqi, category
                FROM air_quality
                WHERE city = %s
                ORDER BY timestamp DESC
                LIMIT 1
            """, (city,))
            row = cur.fetchone()
    return AQIRecord(
        city=row[0], timestamp=row[1], aqi=row[2], category=row[3]
    )

@app.get("/weather/history", response_model=List[WeatherReading])
def get_weather_history(city: str, days: int = Query(3, ge=1, le=30)):
    since = datetime.utcnow() - timedelta(days=days)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT city, timestamp, temperature, humidity, pressure, wind_speed
                FROM weather
                WHERE city = %s AND timestamp >= %s
                ORDER BY timestamp ASC
            """, (city, since))
            rows = cur.fetchall()
    return [WeatherReading(
        city=row[0], timestamp=row[1], temperature=row[2],
        humidity=row[3], pressure=row[4], wind_speed=row[5]
    ) for row in rows]

@app.get("/aqi/history", response_model=List[AQIRecord])
def get_aqi_history(city: str, days: int = Query(3, ge=1, le=30)):
    since = datetime.utcnow() - timedelta(days=days)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT city, timestamp, aqi, category
                FROM air_quality
                WHERE city = %s AND timestamp >= %s
                ORDER BY timestamp ASC
            """, (city, since))
            rows = cur.fetchall()
    return [AQIRecord(
        city=row[0], timestamp=row[1], aqi=row[2], category=row[3]
    ) for row in rows]
