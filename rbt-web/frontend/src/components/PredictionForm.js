import React, { useState } from 'react';

const PredictionForm = ({ onPredict }) => {
  const [industry, setIndustry] = useState('');
  const [renewables, setRenewables] = useState('');
  const [population, setPopulation] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onPredict) {
      onPredict({ industry, renewables, population });
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Predict Carbon Emissions</h2>
      <label>
        Industry:
        <input type="number" value={industry} onChange={e => setIndustry(e.target.value)} required />
      </label>
      <label>
        Renewables:
        <input type="number" value={renewables} onChange={e => setRenewables(e.target.value)} required />
      </label>
      <label>
        Population:
        <input type="number" value={population} onChange={e => setPopulation(e.target.value)} required />
      </label>
      <button type="submit">Predict</button>
    </form>
  );
};

export default PredictionForm; 