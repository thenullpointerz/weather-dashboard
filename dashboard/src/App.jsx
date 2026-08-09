import { useEffect, useState } from 'react';
import './App.css';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const DATA_URL = 'https://raw.githubusercontent.com/thenullpointerz/weather-dashboard/master/weather_data.json';

const WEATHER_CODES = {
  0: 'Clear sky',
  1: 'Mostly clear',
  2: 'Partly cloudy',
  3: 'Cloudy',
  45: 'Fog',
  48: 'Fog',
  51: 'Light drizzle',
  53: 'Moderate drizzle',
  55: 'Dense drizzle',
  61: 'Light rain',
  63: 'Moderate rain',
  65: 'Heavy rain',
  71: 'Light snow',
  73: 'Moderate snow',
  75: 'Heavy snow',
  80: 'Light showers',
  81: 'Moderate showers',
  82: 'Violent showers',
  95: 'Thunderstorm',
  96: 'Thunderstorm with hail',
  99: 'Thunderstorm with hail',
};

function describeWeather(code) {
  return WEATHER_CODES[code] ?? 'Unknown';
}

function App() {
  const [weather, setWeather] = useState(null);

  useEffect(() => {
    fetch(DATA_URL)
      .then((res) => res.json())
      .then((data) => setWeather(data))
      .catch((err) => console.error('Error fetching weather:', err));
  }, []);

  if (!weather) {
    return <div>Loading...</div>;
  }

  const { current } = weather;

  return (
    <div className="dashboard">
      <h1>{current.temperature}°C</h1>
      <p>{describeWeather(current.weather_code)}</p>
      <p>Wind: {current.wind_speed} km/h</p>
      {weather.summary && <p className="summary">{weather.summary}</p>}
       <h2>7-Day Forecast</h2>

      <div className="daily-forecast">
        {weather.daily.map((day) => (
          <div key={day.date} className="daily-card">
            <p>{day.date}</p>
            <p>{describeWeather(day.code)}</p>
            <p>{day.temp_max}° / {day.temp_min}°</p>
          </div>
        ))}
        </div>

      <h2>Hourly Forecast</h2>
      <div className="hourly-forecast">
        {weather.hourly.slice(0, 24).map((hour) => (
          <div key={hour.time} className="hourly-card">
            <p>{hour.time.slice(11)}</p>
            <p>{hour.temp}°</p>
          </div>
        ))}
      </div>

      <h2>Temperature Trend</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={weather.daily}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="temp_max" stroke="#e74c3c" name="Max °C" />
          <Line type="monotone" dataKey="temp_min" stroke="#3498db" name="Min °C" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default App;