// src/App.js

import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [weather, setWeather] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/weather/latest?city=San Francisco")
      .then(res => res.json())
      .then(data => setWeather(data))
      .catch(err => console.error("Weather fetch failed", err));
  }, []);

  return (
    <div className="App">
      <h1>🌍 AtmosStream Dashboard</h1>

      <section>
        <h2>🌤 Weather (San Francisco)</h2>
        {weather ? (
          <ul>
            <li><strong>Temperature:</strong> {weather.temperature}°C</li>
            <li><strong>Humidity:</strong> {weather.humidity}%</li>
            <li><strong>Pressure:</strong> {weather.pressure} hPa</li>
            <li><strong>Wind Speed:</strong> {weather.wind_speed} m/s</li>
            <li><small>Last updated: {new Date(weather.timestamp).toLocaleString()}</small></li>
          </ul>
        ) : (
          <p>Loading weather...</p>
        )}
      </section>
    </div>
  );
}

export default App;
