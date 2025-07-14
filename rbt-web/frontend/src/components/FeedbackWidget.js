import React, { useState } from 'react';

const StarRating = ({ value, onChange }) => (
  <div>
    {[1,2,3,4,5].map(star => (
      <span
        key={star}
        style={{ cursor: 'pointer', color: value >= star ? 'gold' : 'gray', fontSize: 24 }}
        onClick={() => onChange(star)}
      >★</span>
    ))}
  </div>
);

const FeedbackWidget = ({ predictionId }) => {
  const [rating, setRating] = useState(0);
  const [submitted, setSubmitted] = useState(false);

  const submitFeedback = async () => {
    // TODO: Call API
    setSubmitted(true);
  };

  return (
    <div className="feedback-card">
      <h3>How accurate was this prediction?</h3>
      <StarRating value={rating} onChange={setRating} />
      <button onClick={submitFeedback} disabled={submitted}>Submit Rating</button>
      <div className="points-counter">Your contribution score: 250</div>
      {submitted && <div>Thank you for your feedback!</div>}
    </div>
  );
};

export default FeedbackWidget; 