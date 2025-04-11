# AtmosStream: Real-Time Air Quality & Weather Dashboard

**AtmosStream** is a full-stack real-time data platform that fetches and displays weather and air quality data for multiple cities. It uses a distributed backend pipeline, PostgreSQL for storage, a FastAPI backend, and a React frontend with beautiful visualizations.

---

## Features

- Real-time weather and AQI data ingestion from OpenWeatherMap and AirNow
- PostgreSQL-backed time-series storage
- REST API via FastAPI for frontend consumption
- Beautiful React dashboard with real-time graphs
- Multi-city dropdown support
- 2x2 chart layout for temperature, humidity, pressure, and wind speed
- Optional: Apache Beam for distributed ingestion
- Modular codebase, good for testing and scaling

---

## Structure

```
atmostream/
├── ingestion/             # Data ingestion pipelines
│   ├── stream_pipeline.py
│   └── beam_pipeline.py
├── api/                   # FastAPI app
│   ├── main.py
│   ├── models.py
├── database/              # DB schema and utils
│   ├── db_utils.py
│   └── schema.sql
├── frontend/              # React app (runs on port 3002)
│   └── src/
│       ├── App.js
│       └── components/
├── tests/                 # Unit tests
│   ├── test_api.py
│   └── test_db.py
├── .env                   # API keys and DB config (not committed)
├── requirements.txt       # Python backend dependencies
├── docker-compose.yml     # (Optional) container setup
├── package.json           # React frontend dependencies
└── README.md
```

---

## Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/atmostream.git
cd atmostream
```

### 2. Set up the backend

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create your `.env` file:

```env
OPENWEATHER_API_KEY=your_openweather_api_key
AIRNOW_API_KEY=your_airnow_api_key
DATABASE_URL=postgresql://youruser:yourpass@localhost:5432/atmosdb
```

### 3. Set up the PostgreSQL database

```bash
createdb atmosdb
psql -d atmosdb -f database/schema.sql
```

### 4. Run the backend server

```bash
uvicorn api.main:app --reload
```

Server will run at: [http://localhost:8000](http://localhost:8000)

---

## Ingest Data

To pull fresh data from OpenWeather and AirNow:

```bash
python -m ingestion.stream_pipeline
```

Or use Apache Beam (optional):

```bash
python -m ingestion.beam_pipeline
```

---

##  Set up the frontend

```bash
cd frontend
npm install
npm start
```

React app will run at: [http://localhost:3002](http://localhost:3002)

---

## Testing

```bash
pytest tests/
```

---

## Notes

- Requires Python 3.10+
- Make sure PostgreSQL is running locally
- Set correct port (3002) when using frontend with API
- `.env` should **not** be committed (it's in `.gitignore`)

---

## Dashboard Preview

See live city-wise metrics with real-time line charts for:

- Temperature
- Humidity
- Wind Speed
- Pressure

Displayed in a clean 2x2 grid layout.

---

## 👩‍💻 Built By

Eleanor Wiesler  
[eleanorwiesler.com](https://eleanorwiesler.com)  
