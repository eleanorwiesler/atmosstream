import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [weather, setWeather] = useState(null);
  const [city, setCity] = useState("San Francisco");

  const cities = ["San Francisco", "New York", "Chicago", "Los Angeles", "Austin"];

  useEffect(() => {
    fetch(`http://localhost:8000/weather/latest?city=${encodeURIComponent(city)}`)
      .then(res => res.json())
      .then(data => {
        console.log("🌡️ Weather data:", data);
        setWeather(data);
      })
      .catch(err => console.error("❌ Weather fetch failed:", err));
  }, [city]);

  return (
    <div className="App">
      <h1>🌍 AtmosStream Dashboard</h1>

      <section>
        <label htmlFor="city">Select City: </label>
        <select id="city" value={city} onChange={(e) => setCity(e.target.value)}>
          {cities.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </section>

      <section>
        <h2>🌤 Weather ({city})</h2>
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
