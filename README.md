# AtmosStream: Real-Time Air Quality & Weather Dashboard

AtmosStream is a project I built to track air quality and weather conditions across cities in real time. It pulls data from public APIs, stores it in a database, and shows everything in a clean React dashboard. I started this because I care about climate and environmental transparency—this kind of data should be easy to access and understand.

## What it does

- Pulls live data from OpenWeatherMap and AirNow
- Stores everything in a PostgreSQL database
- Serves it via a FastAPI backend
- Displays real-time graphs in a React frontend
- Supports switching between cities
- Tracks temperature, humidity, pressure, and wind speed
- Optional Beam pipeline if you want to scale things up

## Folder structure

```
atmostream/
├── ingestion/             # Scripts to fetch and process API data
│   ├── stream_pipeline.py
│   └── beam_pipeline.py   # (Optional) for Apache Beam setup
├── api/                   # FastAPI backend
│   ├── main.py
│   ├── models.py
├── database/              # DB schema and utility functions
│   ├── db_utils.py
│   └── schema.sql
├── frontend/              # React frontend (runs on port 3002)
│   └── src/
│       ├── App.js
│       └── components/
├── tests/                 # Unit tests
│   ├── test_api.py
│   └── test_db.py
├── .env                   # API keys + DB URL (not committed)
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Optional Docker setup
├── package.json           # React dependencies
└── README.md
```

## Getting it running

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

Create a `.env` file in the root folder with this:

```
OPENWEATHER_API_KEY=your_openweather_api_key
AIRNOW_API_KEY=your_airnow_api_key
DATABASE_URL=postgresql://youruser:yourpass@localhost:5432/atmosdb
```

### 3. Set up the database

```bash
createdb atmosdb
psql -d atmosdb -f database/schema.sql
```

### 4. Run the backend

```bash
uvicorn api.main:app --reload
```

You can now visit: http://localhost:8000

## Pulling in live data

To start pulling real-time weather and air quality data:

```bash
python -m ingestion.stream_pipeline
```

(Or use the Beam version if that’s your thing:)

```bash
python -m ingestion.beam_pipeline
```

## Running the frontend

```bash
cd frontend
npm install
npm start
```

This runs the dashboard on http://localhost:3002

## Running tests

```bash
pytest tests/
```

## A few notes

- Python 3.10+ required
- PostgreSQL needs to be running
- `.env` should never be committed (it’s gitignored)
- Frontend runs on 3002, backend on 8000

## Why I made this

I wanted to build something real around climate data—something useful and understandable. Weather and air quality affect all of us, and this dashboard makes that data feel more tangible. If you have ideas for improvements or want to build on it, feel free to reach out.


---

## 👩‍💻 Built By

Eleanor Wiesler  
[eleanorwiesler.com](https://eleanorwiesler.com)  
