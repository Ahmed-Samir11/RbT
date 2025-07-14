export const setToken = (token) => {
  localStorage.setItem('rbt_token', token);
};

export const getToken = () => {
  return localStorage.getItem('rbt_token');
};

export const clearToken = () => {
  localStorage.removeItem('rbt_token');
}; 