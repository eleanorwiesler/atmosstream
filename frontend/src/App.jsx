// src/App.jsx

import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [weather, setWeather] = useState(null);
  const [aqi, setAqi] = useState(null);

  const city = "San Francisco";

  useEffect(() => {
    fetch(`http://localhost:8000/weather/latest?city=${city}`)
      .then(res => res.json())
      .then(setWeather);

    fetch(`http://localhost:8000/aqi/latest?city=${city}`)
      .then(res => res.json())
      .then(setAqi);
  }, []);

  return (
    <div className="App">
      <h1>AtmosStream Dashboard</h1>

      <section>
        <h2>🌤 Weather</h2>
        {weather ? (
          <ul>
            <li>Temperature: {weather.temperature} °C</li>
            <li>Humidity: {weather.humidity} %</li>
            <li>Pressure: {weather.pressure} hPa</li>
            <li>Wind Speed: {weather.wind_speed} m/s</li>
          </ul>
        ) : <p>Loading weather...</p>}
      </section>

      <section>
        <h2>🫁 Air Quality</h2>
        {aqi ? (
          <ul>
            <li>AQI: {aqi.aqi}</li>
            <li>Category: {aqi.category}</li>
          </ul>
        ) : <p>Loading AQI...</p>}
      </section>
    </div>
  );
}

export default App;
