// src/hooks/useAuth.js
import { useState, useEffect } from 'react';



export const useAuth = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loadingAuth, setLoadingAuth] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      // Try to get user from localStorage or a session cookie
      // For this demo, we'll just use the MOCK_LOGGED_IN_USER
      // You can switch MOCK_LOGGED_IN_USER to null to test logged-out state
      const storedUser = localStorage.getItem('currentUser');
      if (storedUser) {
        setCurrentUser(JSON.parse(storedUser));
      } else {
         setCurrentUser(null);
      }
      setLoadingAuth(false);
    }, 500);
  }, []);

  const login = (username, token, isAdmin = false) => {
    const user = { username, token, isAdmin };
    setCurrentUser(user);
    localStorage.setItem('currentUser', JSON.stringify(user));
  };

  const logout = () => {
    setCurrentUser(null);
    localStorage.removeItem('currentUser');
  };




  return { currentUser, loadingAuth, login, logout };
};