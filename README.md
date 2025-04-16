# AtmosStream: Real-Time Air Quality & Weather Dashboard

AtmosStream is a project I built to track real-time weather and air quality data across cities. It started as a way for me to learn more about building full-stack systems, but also because I care about making environmental data more visible and accessible.

The setup is pretty straightforward: I use public APIs (OpenWeatherMap and AirNow) to fetch data, store it in a PostgreSQL database, and serve it through a FastAPI backend. A React frontend queries the API and displays everything in a clean dashboard with live-updating charts for temperature, humidity, pressure, and wind speed. You can select different cities from a dropdown and see how things change throughout the day.

The backend lives in the `api/` directory, and the ingestion scripts that fetch new data are in `ingestion/`. There's also an optional Apache Beam version of the pipeline if you want to run things in a more distributed way, though I mostly used the simpler version. The frontend React app is in `frontend/` and runs on port 3002. Tests are included too — they're basic but useful.

To run it locally, you’ll need Python 3.10 and Node. First, clone the repo:

```bash
git clone https://github.com/your-username/atmostream.git
cd atmostream
```

Set up a virtual environment and install the backend requirements:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the root directory:

```
OPENWEATHER_API_KEY=your_openweather_api_key
AIRNOW_API_KEY=your_airnow_api_key
DATABASE_URL=postgresql://youruser:yourpass@localhost:5432/atmosdb
```

Then set up your PostgreSQL database:

```bash
createdb atmosdb
psql -d atmosdb -f database/schema.sql
```

Start the FastAPI backend:

```bash
uvicorn api.main:app --reload
```

To pull in new data, run the ingestion script:

```bash
python -m ingestion.stream_pipeline
```

(Or, if you want to try the Beam version for distributed processing:)

```bash
python -m ingestion.beam_pipeline
```

Now switch to the frontend and get it running:

```bash
cd frontend
npm install
npm start
```

This will launch the dashboard at [http://localhost:3002](http://localhost:3002). The API runs on [http://localhost:8000](http://localhost:8000).

To run tests:

```bash
pytest tests/
```

I tried to keep the code modular and readable so it’s easy to extend or plug in new data sources. The project isn’t meant to be production-grade, but it works well and is pretty easy to build on.

If you're interested in environmental monitoring, or just want to explore building a full-stack data pipeline, feel free to use or adapt it. I’d love to hear any feedback or ideas for improving it.

![Alt text](atmos.png)



