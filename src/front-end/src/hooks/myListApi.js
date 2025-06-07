const API_BASE_URL = 'http://localhost:8000/api/user'; // Your backend URL
const getAuthHeaders = (token) => {
  const headers = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
};
export const fetchMyList = async (token) => {
  if (!token) throw new Error("Authentication token is required to fetch my list.");
  const response = await fetch(`${API_BASE_URL}/user-favorites`, {
    headers: getAuthHeaders(token),
  });
  if (!response.ok) {
    const errData = await response.json().catch(() => ({ detail: "Unknown error fetching my list" }));
    throw new Error(errData.detail || `Failed to fetch my list: ${response.status}`);
  }
  return await response.json();
};

export const addToMyList = async ({ movieId, token }) => {
  if (!movieId || !token) {
    throw new Error("Movie ID and authentication token are required to add to my list.");
  }
  const response = await fetch(`${API_BASE_URL}/add-favorite`, {
    method: 'POST',
    headers: getAuthHeaders(token),
    body: JSON.stringify({ movie_id: movieId }),
  });
  if (!response.ok) {
    const errData = await response.json().catch(() => ({ detail: "Unknown error adding to my list" }));
    throw new Error(errData.detail || `Failed to add to my list: ${response.status}`);
  }
  return await response.json();
};

export const removeFromMyList = async ({ movieId, token }) => {
  if (!movieId || !token) {
    throw new Error("Movie ID and authentication token are required to remove from my list.");
  }
  const response = await fetch(`${API_BASE_URL}/remove-favorite`, {
    method: 'DELETE',
    headers: getAuthHeaders(token),
    body: JSON.stringify({ movie_id: movieId }),
  });
  if (!response.ok) {
    const errData = await response.json().catch(() => ({ detail: "Unknown error removing from my list" }));
    throw new Error(errData.detail || `Failed to remove from my list: ${response.status}`);
  }
  return await response.json();
};