// src/services/commentApi.js
const API_BASE_URL = 'http://localhost:8000/api'; // Your backend URL

const getAuthHeaders = (token) => {
  const headers = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
};

export const fetchCommentsByMovieId = async (movieId) => {
  if (!movieId) throw new Error("Movie ID is required for fetching comments.");
  const response = await fetch(`${API_BASE_URL}/comments/movie/${movieId}`);
  if (!response.ok) {
    const errData = await response.json().catch(() => ({ detail: "Unknown error fetching comments" }));
    throw new Error(errData.detail || `Failed to fetch comments: ${response.status}`);
  }
  const data = await response.json();
  return data.comments || []; // API returns { comments: [...], total: count }
};

export const createComment = async ({ movieId, commentText, token }) => {
  if (!movieId || !commentText || !token) {
    throw new Error("Movie ID, comment text, and token are required to create a comment.");
  }
  const response = await fetch(`${API_BASE_URL}/comment`, {
    method: 'POST',
    headers: getAuthHeaders(token),
    body: JSON.stringify({
      movie_id: movieId,
      comment_text: commentText,
    }),
  });
  if (!response.ok) {
    const errData = await response.json().catch(() => ({ detail: "Unknown error creating comment" }));
    throw new Error(errData.detail || `Failed to post comment: ${response.status}`);
  }
  return await response.json();
};

export const deleteCommentAPI = async ({ commentId, token }) => { // Renamed to avoid conflict
  if (!commentId || !token) {
    throw new Error("Comment ID and token are required to delete a comment.");
  }
  const response = await fetch(`${API_BASE_URL}/comment/${commentId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(token), // Only token needed in headers usually
  });
  if (!response.ok) {
    const errData = await response.json().catch(() => ({ detail: "Unknown error deleting comment" }));
    throw new Error(errData.detail || `Failed to delete comment: ${response.status}`);
  }
  return await response.json();
};

export const updateCommentAPI = async ({ commentId, commentText, token }) => { // Renamed
  if (!commentId || !commentText || !token) {
    throw new Error("Comment ID, text, and token are required to update a comment.");
  }
  const response = await fetch(`${API_BASE_URL}/comment`, {
    method: 'PUT',
    headers: getAuthHeaders(token),
    body: JSON.stringify({
      comment_id: commentId,
      comment_text: commentText,
    }),
  });
  if (!response.ok) {
    const errData = await response.json().catch(() => ({ detail: "Unknown error updating comment" }));
    throw new Error(errData.detail || `Failed to update comment: ${response.status}`);
  }
  return await response.json();
};