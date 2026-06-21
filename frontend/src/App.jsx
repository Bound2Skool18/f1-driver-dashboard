import { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {
  const [driver1, setDriver1] = useState('VER');
  const [driver2, setDriver2] = useState('LEC');
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(false);

  async function handleCompare() {
    setLoading(true);
    const url = `http://127.0.0.1:8000/compare?year=2024&race=Monza&driver_1=${driver1}&driver_2=${driver2}`;
    const response = await fetch(url);
    const data = await response.json();

    const merged = data.distance.map((d, i) => ({
      distance: d,
      [driver1]: data.driver_1_speed[i],
      [driver2]: data.driver_2_speed[i],
    }));

    setChartData(merged);
    setLoading(false);
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>F1 Driver Comparison</h1>

      <div style={{ marginBottom: '1rem' }}>
        <label>
          Driver 1:{' '}
          <input value={driver1} onChange={(e) => setDriver1(e.target.value.toUpperCase())} />
        </label>
        {' '}
        <label>
          Driver 2:{' '}
          <input value={driver2} onChange={(e) => setDriver2(e.target.value.toUpperCase())} />
        </label>
        {' '}
        <button onClick={handleCompare} disabled={loading}>
          {loading ? 'Loading...' : 'Compare'}
        </button>
      </div>

      {chartData.length > 0 && (
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData}>
            <XAxis dataKey="distance" label={{ value: 'Distance (m)', position: 'insideBottom', offset: -5 }} />
            <YAxis label={{ value: 'Speed (km/h)', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey={driver1} stroke="#3b82f6" dot={false} />
            <Line type="monotone" dataKey={driver2} stroke="#ef4444" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}

export default App;