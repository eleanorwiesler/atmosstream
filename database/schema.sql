-- schema.sql

CREATE TABLE IF NOT EXISTS weather (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100),
    timestamp TIMESTAMPTZ,
    temperature FLOAT,
    humidity FLOAT,
    pressure FLOAT,
    wind_speed FLOAT
);

CREATE TABLE IF NOT EXISTS air_quality (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100),
    timestamp TIMESTAMPTZ,
    aqi INTEGER,
    category VARCHAR(100)
);
