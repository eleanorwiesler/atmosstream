# api/models.py

from pydantic import BaseModel
from datetime import datetime
from typing import List

class WeatherReading(BaseModel):
    city: str
    timestamp: datetime
    temperature: float
    humidity: float
    pressure: float
    wind_speed: float

class AQIRecord(BaseModel):
    city: str
    timestamp: datetime
    aqi: int
    category: str
