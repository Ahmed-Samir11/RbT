import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const getToken = async (user_id) => {
  const res = await axios.post(`${API_URL}/token`, { user_id });
  return res.data.access_token;
};

export const predict = async (data, token) => {
  const res = await axios.post(`${API_URL}/predict`, data, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return res.data;
};

export const submitFeedback = async (prediction_id, actual_emissions, rating, token) => {
  const res = await axios.post(`${API_URL}/feedback`, { prediction_id, actual_emissions, rating }, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return res.data;
}; 