# ingestion/beam_pipeline.py

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from datetime import datetime
from database.db_utils import insert_weather

class FetchWeatherDoFn(beam.DoFn):
    def process(self, element):
        import requests, os
        from dotenv import load_dotenv
        load_dotenv()

        city = element
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        r = requests.get(url).json()
        
        yield {
            "city": city,
            "timestamp": datetime.utcnow(),
            "temperature": r["main"]["temp"],
            "humidity": r["main"]["humidity"],
            "pressure": r["main"]["pressure"],
            "wind_speed": r["wind"]["speed"]
        }

class WriteToPostgresDoFn(beam.DoFn):
    def process(self, element):
        insert_weather(element)

def run():
    options = PipelineOptions()
    cities = ["San Francisco", "New York"]

    with beam.Pipeline(options=options) as p:
        (
            p
            | "Create city list" >> beam.Create(cities)
            | "Fetch weather" >> beam.ParDo(FetchWeatherDoFn())
            | "Write to DB" >> beam.ParDo(WriteToPostgresDoFn())
        )

if __name__ == "__main__":
    run()
