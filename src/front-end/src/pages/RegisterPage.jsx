import React, { useState } from 'react';
import Input from '../components/Input';
import Button from '../components/Button';
import GoogleIcon from '../components/icons/GoogleIcon';
import UserIcon from '../components/icons/UserIcon'; // Changed from MailIcon
import LockIcon from '../components/icons/LockIcon'; // Import LockIcon for password fields
import { useNavigate } from 'react-router-dom'; // Import useNavigate for navigation
// UserIcon is already imported, no need to import it twice (one was for Full Name)
// Removed: import type { Page } from '../App'; // Import Page type

const FilmReelIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" {...props}>
    <path d="M18 3H6C4.346 3 3 4.346 3 6V18C3 19.654 4.346 21 6 21H18C19.654 21 21 19.654 21 18V6C21 4.346 19.654 3 18 3ZM7 17H5V15H7V17ZM7 13H5V11H7V13ZM7 9H5V7H7V9ZM15 17H9V7H15V17ZM19 17H17V15H19V17ZM19 13H17V11H19V13ZM19 9H17V7H19V9Z"/>
  </svg>
);

// Removed RegisterPageProps interface

const RegisterPage = () => {
  const [fullName, setFullName] = useState('');
  const [username, setUsername] = useState(''); // Changed from email
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [passwordError, setPasswordError] = useState(null);

  const navigateTo = useNavigate(); // Use useNavigate for navigation
  const handleRegister = async (e) => {
    e.preventDefault();
    setError(null);
    setPasswordError(null);

    if (password !== confirmPassword) {
      setPasswordError("Passwords do not match.");
      return;
    }

    setIsLoading(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    // Dummy registration logic
    if (username === 'takenusername') { // Changed from email === 'taken@example.com'
      setError('This username is already taken.'); // Changed error message
      console.error('Registration failed: Username taken');
    } else {
      console.log('Registration successful:', { fullName, username });
      // Potentially navigate to login or a success page
      alert('Registration successful! Please login.');
      navigateTo('login');
    }
    setIsLoading(false);
  };

  const handleGoogleRegister = () => {
    console.log('Register with Google clicked');
    // Actual Google registration logic would be implemented here
  };

  const handleLoginClick = (e) => {
    e.preventDefault();
    navigateTo('/login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-neutral-900 to-neutral-800 flex flex-col justify-center items-center p-4 text-gray-100 selection:bg-red-500 selection:text-white">
      <div className="w-full max-w-md bg-neutral-800/80 backdrop-blur-lg shadow-2xl rounded-xl p-8 sm:p-10 space-y-6">
        <div className="text-center">
          <FilmReelIcon className="h-16 w-16 mx-auto text-red-500 mb-3" />
          <h1 className="text-3xl font-bold text-white">CineSuggest</h1>
          <p className="text-neutral-400 mt-1">Create your account to start discovering</p>
        </div>

        {error && (
          <div className="bg-red-500/20 border border-red-500 text-red-300 px-4 py-3 rounded-lg text-sm" role="alert">
            <p>{error}</p>
          </div>
        )}

        <form onSubmit={handleRegister} className="space-y-6">
          <Input
            id="fullName"
            type="text"
            label="Full Name"
            placeholder="John Doe"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            icon={<UserIcon className="h-5 w-5" />} // UserIcon for full name
            required
            disabled={isLoading}
            aria-required="true"
          />
          <Input
            id="username-register" // Changed from email-register
            type="text" // Changed from email
            label="Username" // Changed from Email Address
            placeholder="yourusername" // Changed from you@example.com
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            icon={<UserIcon className="h-5 w-5" />} // Changed from MailIcon to UserIcon
            required
            disabled={isLoading}
            aria-required="true"
            aria-invalid={!!error}
            aria-describedby={error ? "register-error" : undefined}
          />
          <Input
            id="password-register"
            type="password"
            label="Password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              if (passwordError) setPasswordError(null);
            }}
            icon={<LockIcon className="h-5 w-5" />}
            required
            disabled={isLoading}
            aria-required="true"
            aria-invalid={!!passwordError}
            aria-describedby={passwordError ? "password-match-error" : undefined}
          />
          <Input
            id="confirmPassword"
            type="password"
            label="Confirm Password"
            placeholder="••••••••"
            value={confirmPassword}
            onChange={(e) => {
              setConfirmPassword(e.target.value);
              if (passwordError) setPasswordError(null);
            }}
            icon={<LockIcon className="h-5 w-5" />}
            required
            disabled={isLoading}
            error={passwordError}
            aria-required="true"
            aria-invalid={!!passwordError}
            aria-describedby={passwordError ? "password-match-error" : undefined}
          />
          {passwordError && <p id="password-match-error" className="sr-only">{passwordError}</p>}

          <Button
            type="submit"
            variant="primary"
            fullWidth
            isLoading={isLoading}
            disabled={isLoading}
          >
            {isLoading ? 'Registering...' : 'Register'}
          </Button>
        </form>
        {error && <p id="register-error" className="sr-only">{error}</p>}

        <p className="text-sm text-center text-neutral-400">
          Already have an account?{' '}
          <a href="#login" onClick={handleLoginClick} className="font-medium text-red-500 hover:text-red-400 hover:underline">
            Login here
          </a>
        </p>
      </div>
       <footer className="absolute bottom-4 text-center text-xs text-neutral-500 w-full">
        © {new Date().getFullYear()} CineSuggest. All rights reserved.
      </footer>
    </div>
  );
};

export default RegisterPage;