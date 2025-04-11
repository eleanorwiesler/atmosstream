# ingestion/beam_pipeline.py

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from datetime import datetime
import os
import requests
from dotenv import load_dotenv
from database.db_utils import insert_weather

# Load environment variables
load_dotenv()

class FetchWeatherDoFn(beam.DoFn):
    def process(self, city):
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            r = requests.get(url).json()
            yield {
                "city": city,
                "timestamp": datetime.utcnow(),
                "temperature": r["main"]["temp"],
                "humidity": r["main"]["humidity"],
                "pressure": r["main"]["pressure"],
                "wind_speed": r["wind"]["speed"]
            }
        except Exception as e:
            print(f"[❌] Failed for {city}: {e}")

def run():
    cities = ["San Francisco", "Chicago", "New York", "Los Angeles", "Austin"]
    options = PipelineOptions()

    with beam.Pipeline(options=options) as p:
        (
            p
            | "Create city list" >> beam.Create(cities)
            | "Fetch weather" >> beam.ParDo(FetchWeatherDoFn())
            | "Write to DB" >> beam.Map(insert_weather)
        )

if __name__ == "__main__":
    run()
