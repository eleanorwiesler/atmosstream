import React, { useEffect, useState } from 'react';
import './App.css';
import Select from 'react-select';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Legend,
  Tooltip
} from 'chart.js';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Legend, Tooltip);

function App() {
  const [weather, setWeather] = useState(null);
  const [city, setCity] = useState("San Francisco");
  const [history, setHistory] = useState([]);

  const cities = ["San Francisco", "Chicago", "New York", "Los Angeles", "Austin"];
  const cityOptions = cities.map((c) => ({ label: c, value: c }));

  useEffect(() => {
    const fetchWeather = () => {
      fetch(`http://localhost:8000/weather/latest?city=${encodeURIComponent(city)}`)
        .then(res => res.json())
        .then(data => setWeather(data))
        .catch(err => console.error("❌ Weather fetch failed:", err));
    };

    fetchWeather();
    const interval = setInterval(fetchWeather, 60_000);
    return () => clearInterval(interval);
  }, [city]);

  useEffect(() => {
    const fetchHistory = () => {
      fetch(`http://localhost:8000/weather/history?city=${encodeURIComponent(city)}`)
        .then(res => res.json())
        .then(data => setHistory(data))
        .catch(err => console.error("❌ Weather history fetch failed:", err));
    };

    fetchHistory();
    const interval = setInterval(fetchHistory, 60_000);
    return () => clearInterval(interval);
  }, [city]);

  const timeLabels = history.map(h =>
    new Date(h.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  );

  const makeChart = (label, color, values) => ({
    labels: timeLabels,
    datasets: [
      {
        label,
        data: values,
        borderColor: color,
        tension: 0.2,
        pointRadius: 3,
        borderWidth: 2
      }
    ]
  });

  return (
    <div className="App" style={{ maxWidth: 1200, margin: "0 auto", padding: "2rem" }}>
      <h1 style={{ textAlign: "center", marginBottom: "2rem" }}>AtmosStream Dashboard</h1>

      <section style={{ marginBottom: "3rem", maxWidth: 400, marginInline: "auto" }}>
        <label htmlFor="city" style={{ display: "block", fontWeight: 600, marginBottom: "0.5rem" }}>
          Select City:
        </label>
        <Select
          options={cityOptions}
          defaultValue={cityOptions.find(opt => opt.value === city)}
          onChange={(selected) => setCity(selected.value)}
          styles={{
            control: (base) => ({
              ...base,
              borderRadius: 8,
              padding: '2px 4px',
              borderColor: '#ccc',
              boxShadow: 'none',
              fontSize: '1rem'
            }),
            option: (base, { isFocused }) => ({
              ...base,
              backgroundColor: isFocused ? '#f0f0f0' : 'white',
              color: '#333',
            }),
          }}
        />
      </section>

      <section style={{ marginBottom: "3rem" }}>
        <h2 style={{ marginBottom: "1rem" }}>Current Weather – {city}</h2>
        {weather ? (
          <div style={{ display: "flex", justifyContent: "space-between", flexWrap: "wrap", gap: "1rem" }}>
            <div><strong>Temperature:</strong> {weather.temperature} °C</div>
            <div><strong>Humidity:</strong> {weather.humidity} %</div>
            <div><strong>Pressure:</strong> {weather.pressure} hPa</div>
            <div><strong>Wind Speed:</strong> {weather.wind_speed} m/s</div>
            <div style={{ width: "100%", marginTop: "0.5rem" }}>
              <small>Last updated: {new Date(weather.timestamp).toLocaleString()}</small>
            </div>
          </div>
        ) : (
          <p>Loading weather...</p>
        )}
      </section>

      {history.length > 0 ? (
        <section>
          <h2 style={{ textAlign: "center", marginBottom: "2rem" }}>Past 24-Hour Weather Trends</h2>
          <div style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '2rem',
          }}>
            <div>
              <h4>Temperature (°C)</h4>
              {weather && <p style={{ fontSize: "0.9rem" }}>Current: {weather.temperature} °C</p>}
              <Line data={makeChart("Temperature", "red", history.map(h => h.temperature))} />
            </div>
            <div>
              <h4>Humidity (%)</h4>
              {weather && <p style={{ fontSize: "0.9rem" }}>Current: {weather.humidity} %</p>}
              <Line data={makeChart("Humidity", "blue", history.map(h => h.humidity))} />
            </div>
            <div>
              <h4>Pressure (hPa)</h4>
              {weather && <p style={{ fontSize: "0.9rem" }}>Current: {weather.pressure} hPa</p>}
              <Line data={makeChart("Pressure", "green", history.map(h => h.pressure))} />
            </div>
            <div>
              <h4>Wind Speed (m/s)</h4>
              {weather && <p style={{ fontSize: "0.9rem" }}>Current: {weather.wind_speed} m/s</p>}
              <Line data={makeChart("Wind Speed", "purple", history.map(h => h.wind_speed))} />
            </div>
          </div>
        </section>
      ) : (
        <p>Loading charts...</p>
      )}
    </div>
  );
}

export default App;
