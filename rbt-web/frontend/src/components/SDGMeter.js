import React from 'react';
// import { Gauge } from '@ant-design/plots';

const SDGMeter = ({ score }) => {
  // Placeholder for Gauge
  // const config = { ... };
  // return <Gauge {...config} />;
  return (
    <div style={{ margin: '20px 0' }}>
      <h3>SDG Score: {score}</h3>
      <div style={{ width: 200, height: 100, background: '#eee', borderRadius: 100, position: 'relative' }}>
        <div style={{
          width: `${score}%`,
          height: '100%',
          background: score > 75 ? 'green' : score > 50 ? 'gold' : 'red',
          borderRadius: 100
        }} />
      </div>
    </div>
  );
};

export default SDGMeter; 