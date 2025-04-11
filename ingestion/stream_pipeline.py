# ingestion/stream_pipeline.py

import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from database.db_utils import insert_weather, insert_aqi

load_dotenv()

def fetch_weather(city="San Francisco"):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    print(f"[AirNow] URL: {url}")

    r = requests.get(url).json()

    return {
        "city": city,
        "timestamp": datetime.utcnow(),
        "temperature": r["main"]["temp"],
        "humidity": r["main"]["humidity"],
        "pressure": r["main"]["pressure"],
        "wind_speed": r["wind"]["speed"]
    }

def fetch_airnow(city="San Francisco"):
    api_key = os.getenv("AIRNOW_API_KEY")

    # Map cities to ZIP codes
    zip_map = {
        "San Francisco": "94103",
        "Chicago": "60601",
        "New York": "10001",
        "Austin": "73301",
        "Los Angeles": "90001"
    }
    zip_code = zip_map.get(city)
    if not zip_code:
        print(f"[AirNow] ❌ No ZIP code for city: {city}")
        return None

    url = f"https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode={zip_code}&distance=25&API_KEY={api_key}"
    print(f"[AirNow] URL: {url}")

    try:
        r = requests.get(url)
        print(f"[AirNow] status: {r.status_code}")
        print(f"[AirNow] response: {r.text[:100]}...")

        if "text/html" in r.headers.get("Content-Type", ""):
            print("[AirNow] ❌ Unexpected response — likely an HTML page.")
            return None

        data = r.json()
        if not data:
            return None

        first = data[0]
        return {
            "city": city,
            "timestamp": datetime.utcnow(),
            "aqi": first["AQI"],
            "category": first["Category"]["Name"]
        }
    except Exception as e:
        print(f"[AirNow] ❌ Error fetching AQI for {city}: {e}")
        return None

def main():
    cities = ["San Francisco", "Chicago", "New York", "Austin", "Los Angeles"]

    for city in cities:
        print(f"\n🌐 Fetching weather for {city}")
        try:
            weather = fetch_weather(city)
            insert_weather(weather)
            print(f"[✓] Weather data inserted for {city}")
        except Exception as e:
            print(f"[❌] Weather failed for {city}: {e}")

        print(f"🌫️  Fetching AQI for {city}")
        try:
            aqi = fetch_airnow(city)
            if aqi:
                insert_aqi(aqi)
                print(f"[✓] AQI data inserted for {city}")
            else:
                print(f"[–] Skipped AQI insert for {city}")
        except Exception as e:
            print(f"[❌] AQI failed for {city}: {e}")

if __name__ == "__main__":
    main()
