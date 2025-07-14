import React from 'react';
import PredictionForm from './PredictionForm';
import FeedbackWidget from './FeedbackWidget';
import SDGMeter from './SDGMeter';
import EvolutionChart from './EvolutionChart';
import RegionalComparison from './RegionalComparison';

const Dashboard = () => (
  <div>
    <h1>Carbon Emission Dashboard</h1>
    <PredictionForm />
    <SDGMeter score={75} />
    <EvolutionChart />
    <RegionalComparison />
    <FeedbackWidget predictionId={null} />
  </div>
);

export default Dashboard; 