import React, { useEffect, useState } from 'react';
import { fetchWeatherBenchEvaluation } from '../services/api';

const WeatherBenchPage = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getData = async () => {
      try {
        setLoading(true);
        const result = await fetchWeatherBenchEvaluation();
        setData(result);
      } catch (err) {
        setError('Failed to fetch WeatherBench evaluation data.');
      } finally {
        setLoading(false);
      }
    };
    getData();
  }, []);

  if (loading) return <div>Loading WeatherBench evaluation...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (!data) return null;

  // Helper to render a table for a model
  const renderTable = (results) => (
    <table style={{ margin: '0 auto', borderCollapse: 'collapse' }}>
      <thead>
        <tr>
          <th style={{ border: '1px solid #ccc', padding: 8 }}>Timestamp</th>
          <th style={{ border: '1px solid #ccc', padding: 8 }}>Prediction</th>
          <th style={{ border: '1px solid #ccc', padding: 8 }}>Ground Truth</th>
          <th style={{ border: '1px solid #ccc', padding: 8 }}>Error</th>
        </tr>
      </thead>
      <tbody>
        {results.map((row, i) => (
          <tr key={i}>
            <td style={{ border: '1px solid #ccc', padding: 8 }}>{row.timestamp}</td>
            <td style={{ border: '1px solid #ccc', padding: 8 }}>{row.prediction.toFixed(2)}</td>
            <td style={{ border: '1px solid #ccc', padding: 8 }}>{row.ground_truth.toFixed(2)}</td>
            <td style={{ border: '1px solid #ccc', padding: 8 }}>{row.error.toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );

  // Simple SVG line chart for predictions vs ground truth
  const renderLineChart = (results, color, label) => {
    const width = 400, height = 120, pad = 30;
    const values = results.map(r => r.prediction);
    const truths = results.map(r => r.ground_truth);
    const maxY = Math.max(...values, ...truths);
    const minY = Math.min(...values, ...truths);
    const scaleX = (i) => pad + (i * (width - 2 * pad)) / (results.length - 1);
    const scaleY = (v) => height - pad - ((v - minY) * (height - 2 * pad)) / (maxY - minY + 1e-6);
    const line = (arr, stroke) => (
      <polyline
        fill="none"
        stroke={stroke}
        strokeWidth="2"
        points={arr.map((v, i) => `${scaleX(i)},${scaleY(v)}`).join(' ')}
      />
    );
    return (
      <svg width={width} height={height} style={{ background: '#f9f9f9', margin: 10 }}>
        {line(values, color)}
        {line(truths, '#888')}
        <text x={pad} y={pad} fontSize="12" fill={color}>{label} (pred)</text>
        <text x={pad} y={pad + 14} fontSize="12" fill="#888">Ground Truth</text>
      </svg>
    );
  };

  // Error chart
  const renderErrorChart = (results, color, label) => {
    const width = 400, height = 80, pad = 30;
    const errors = results.map(r => r.error);
    const maxY = Math.max(...errors);
    const scaleX = (i) => pad + (i * (width - 2 * pad)) / (results.length - 1);
    const scaleY = (v) => height - pad - ((v) * (height - 2 * pad)) / (maxY + 1e-6);
    return (
      <svg width={width} height={height} style={{ background: '#f9f9f9', margin: 10 }}>
        <polyline
          fill="none"
          stroke={color}
          strokeWidth="2"
          points={errors.map((v, i) => `${scaleX(i)},${scaleY(v)}`).join(' ')}
        />
        <text x={pad} y={pad} fontSize="12" fill={color}>{label} Error</text>
      </svg>
    );
  };

  return (
    <div style={{ textAlign: 'center', marginTop: 60 }}>
      <h1>WeatherBench Evaluation</h1>
      <p>Model performance on WeatherBench data (Standard vs Self-Improving):</p>
      <div style={{ display: 'flex', justifyContent: 'center', gap: 40 }}>
        <div>
          <h3>Standard Model</h3>
          {renderLineChart(data.standard.results, '#1976d2', 'Standard')}
          {renderErrorChart(data.standard.results, '#1976d2', 'Standard')}
          <div style={{ margin: '10px 0' }}><strong>MAE:</strong> {data.standard.mae.toFixed(2)}</div>
          {renderTable(data.standard.results)}
        </div>
        <div>
          <h3>Self-Improving Model</h3>
          {renderLineChart(data.self_improving.results, '#43a047', 'Self-Improving')}
          {renderErrorChart(data.self_improving.results, '#43a047', 'Self-Improving')}
          <div style={{ margin: '10px 0' }}><strong>MAE:</strong> {data.self_improving.mae.toFixed(2)}</div>
          {renderTable(data.self_improving.results)}
        </div>
      </div>
    </div>
  );
};

export default WeatherBenchPage; 