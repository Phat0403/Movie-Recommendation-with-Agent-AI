
import React, { useState } from 'react';
import MailIcon from '../components/icons/MailIcon';
import GoogleIcon from '../components/icons/GoogleIcon';
import LockIcon from '../components/icons/LockIcon';
import Button from '../components/Button';
import Input from '../components/Input';
import { useNavigate } from 'react-router-dom'; // Import useNavigate for navigation
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

  const navigate = useNavigate(); // Use useNavigate for navigation
  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    if (username === 'test@example.com' && password === 'password') {
      console.log('Login successful:', { username });
      // Navigate to dashboard or home page
    } else {
      setError('Invalid email or password.');
      console.error('Login failed');
    }
    setIsLoading(false);
  };

  const handleGoogleLogin = () => {
    console.log('Login with Google clicked');
    // Actual Google login logic would be implemented here
    // For example, redirecting to Google's OAuth endpoint
  };

  const handleRegisterClick = (e) => {
    e.preventDefault();
    navigate('/register'); // Navigate to the registration page
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
            type="text"
            label="Username"
            placeholder="Enter your username"
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
            <a href="#" onClick={(e) => {e.preventDefault(); console.log("Forgot password clicked")}} className="text-sm text-sky-500 hover:text-sky-400 hover:underline">
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

        <div className="relative flex items-center py-2">
          <div className="flex-grow border-t border-slate-600"></div>
          <span className="flex-shrink mx-4 text-slate-400 text-xs uppercase">Or continue with</span>
          <div className="flex-grow border-t border-slate-600"></div>
        </div>

        <Button
          type="button"
          variant="google"
          fullWidth
          onClick={handleGoogleLogin}
          icon={<GoogleIcon className="h-5 w-5" />}
          disabled={isLoading}
          className=""
        >
          Login with Google
        </Button>

        <p className="text-sm text-center text-slate-400">
          Don't have an account?{' '}
          <a href="#register" onClick={handleRegisterClick} className="font-medium text-sky-500 hover:text-sky-400 hover:underline">
            Register here
          </a>
        </p>
      </div>
      <footer className="absolute bottom-4 text-center text-xs text-slate-500 w-full">
        &copy; {new Date().getFullYear()} CineSuggest. All rights reserved.
      </footer>
    </div>
  );
};

export default LoginPage;