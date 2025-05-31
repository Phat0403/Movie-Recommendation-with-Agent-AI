import React, { useState, useEffect } from 'react';
import MailIcon from '../components/icons/MailIcon';
import GoogleIcon from '../components/icons/GoogleIcon'; // Assuming GoogleIcon might be used later
import LockIcon from '../components/icons/LockIcon';
import Button from '../components/Button';
import Input from '../components/Input';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

// FilmReelIcon component as provided
const FilmReelIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" {...props}>
    <path d="M18 3H6C4.346 3 3 4.346 3 6V18C3 19.654 4.346 21 6 21H18C19.654 21 21 19.654 21 18V6C21 4.346 19.654 3 18 3ZM7 17H5V15H7V17ZM7 13H5V11H7V13ZM7 9H5V7H7V9ZM15 17H9V7H15V17ZM19 17H17V15H19V17ZM19 13H17V11H19V13ZM19 9H17V7H19V9Z"/>
  </svg>
);

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const auth = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const formData = new URLSearchParams();
      formData.append('username', username); // Corresponds to form_data.username in FastAPI
      formData.append('password', password); // Corresponds to form_data.password in FastAPI

      // Replace '/api/v1' with your actual API prefix if you have one.
      // If your frontend and backend are on different domains during development,
      // you might need to configure CORS on the backend or use a proxy.
      const response = await fetch('http://localhost:8000/api/auth/login', { // Assuming your API endpoint is at /login
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
      });

      const responseData = await response.json(); // Backend returns JSONResponse

      if (response.ok) {
        auth.login(username, responseData.access_token); // Assuming your auth context has a login method
        console.log('Login successful:', responseData);
      } else {
        // Login failed, backend should return an error message
        // FastAPI's HTTPException often provides error details in responseData.detail
        setError(responseData.detail || 'Invalid username or password.');
        console.error('Login failed:', responseData);
      }
    } catch (err) {
      // Network error or other issues with the fetch request
      setError('Login failed. An unexpected error occurred. Please try again.');
      console.error('Login request error:', err);
    } finally {
      setIsLoading(false);
    }
  };
   useEffect(() => {
    if (auth.currentUser) {
      navigate('/'); // Or to a dashboard, or previous intended page
    }
  }, [auth.currentUser, navigate]);


  const handleRegisterClick = (e) => {
    e.preventDefault();
    navigate('/register');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex flex-col justify-center items-center p-4 text-gray-100">
      <div className="w-full max-w-md bg-slate-800/80 backdrop-blur-lg shadow-2xl rounded-xl p-8 sm:p-6 space-y-4">
        <div className="text-center">
          <FilmReelIcon className="h-14 w-14 mx-auto text-sky-500 mb-2" />
          <h1 className="text-3xl font-bold text-white">CineSuggest</h1>
        </div>

        {error && (
          <div className="bg-rose-700/30 border border-rose-600 text-rose-300 px-4 py-3 rounded-lg text-sm" role="alert">
            <p>{error}</p>
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <Input
            id="username"
            type="text" // Changed from email to text to be more generic for "username"
            label="Username or Email"
            placeholder="Enter your username or email"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            icon={<MailIcon className="h-5 w-5" />}
            required
            disabled={isLoading}
            error={undefined}
            className=""
          />
          <Input
            id="password"
            type="password"
            label="Password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            icon={<LockIcon className="h-5 w-5" />}
            required
            disabled={isLoading}
            error={undefined}
            className=""
          />
          <div className="flex items-center justify-end">
            <a href="#" onClick={(e) => {e.preventDefault(); navigate('/reset-password');}} className="text-sm text-sky-500 hover:text-sky-400 hover:underline">
              Forgot password?
            </a>
          </div>
          <Button
            type="submit"
            variant="primary"
            fullWidth
            isLoading={isLoading}
            disabled={isLoading}
            icon={undefined}
            className=""
          >
            {isLoading ? 'Logging in...' : 'Login'}
          </Button>
        </form>
        <p className="text-sm text-center text-slate-400">
          Don't have an account?{' '}
          <a href="#register" onClick={handleRegisterClick} className="font-medium text-sky-500 hover:text-sky-400 hover:underline">
            Register here
          </a>
        </p>
        
      </div>
      <footer className="absolute bottom-4 text-center text-xs text-slate-500 w-full">
        © {new Date().getFullYear()} CineSuggest. All rights reserved.
      </footer>
    </div>
  );
};

export default LoginPage;