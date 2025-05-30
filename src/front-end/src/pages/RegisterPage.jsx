import React, { useState } from 'react';
import Input from '../components/Input';
import Button from '../components/Button';
// import GoogleIcon from '../components/icons/GoogleIcon'; // Kept for context
import UserIcon from '../components/icons/UserIcon'; // Assuming you have this icon
import LockIcon from '../components/icons/LockIcon';
import MailIcon from '../components/icons/MailIcon'; // For Email input
import { useNavigate } from 'react-router-dom';

// FilmReelIcon (Using the one from LoginPage for color consistency)
const FilmReelIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" {...props}>
    <path d="M18 3H6C4.346 3 3 4.346 3 6V18C3 19.654 4.346 21 6 21H18C19.654 21 21 19.654 21 18V6C21 4.346 19.654 3 18 3ZM7 17H5V15H7V17ZM7 13H5V11H7V13ZM7 9H5V7H7V9ZM15 17H9V7H15V17ZM19 17H17V15H19V17ZM19 13H17V11H19V13ZM19 9H17V7H19V9Z"/>
  </svg>
);


const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [email, setEmail] = useState('');
  const [otp, setOtp] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [resendOtpIsLoading, setResendOtpIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [passwordError, setPasswordError] = useState(null);
  const [otpError, setOtpError] = useState(null);
  const [registrationStage, setRegistrationStage] = useState('register');

  const navigateTo = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setPasswordError(null);
    setOtpError(null);

    setIsLoading(true);

    if (registrationStage === 'register') {
      if (password !== confirmPassword) {
        setPasswordError("Passwords do not match.");
        setIsLoading(false);
        return;
      }

      try {
        const response = await fetch("http://localhost:8000/api/auth/initiate-registration", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password, email, is_admin: false })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || data.detail || "Registration initiation failed.");
        setRegistrationStage('verifyOtp');
      } catch (err) {
        console.error("Registration initiation error:", err);
        setError(err.message);
      }
    } else if (registrationStage === 'verifyOtp') {
      try {
        // Note: FastAPI often prefers data in the body for POST, even if simple.
        // If your backend strictly requires query params for this POST, keep it.
        // Otherwise, consider sending username and code in the body.
        const response = await fetch(`http://localhost:8000/api/auth/verify-otp-and-register?username=${encodeURIComponent(username)}&code=${encodeURIComponent(otp)}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" }
          // body: JSON.stringify({ username, code: otp }) // Alternative if backend supports body
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || data.detail || "OTP verification failed.");
        navigateTo("/login");
      } catch (err) {
        console.error("OTP verification error:", err);
        setOtpError(err.message);
      }
    }
    setIsLoading(false);
  };

  const handleResendOtp = async () => {
    setResendOtpIsLoading(true);
    setOtpError(null);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/api/auth/resend-registration-otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || data.detail || "Failed to resend OTP.");
      // Consider a more subtle notification than alert, maybe a temporary success message
      alert("A new OTP has been sent to your email.");
    } catch (err) {
      console.error("Resend OTP error:", err);
      setOtpError(err.message); // Show resend error in the OTP error slot
    }
    setResendOtpIsLoading(false);
  };

  const handleLoginClick = (e) => {
    e.preventDefault();
    navigateTo('/login');
  };

  // Common error display for general errors and OTP errors
  const displayError = error || otpError; // Password error is handled by Input component directly

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex flex-col justify-center items-center p-4 text-gray-100 selection:bg-sky-500 selection:text-white"> {/* Changed selection color */}
      <div className="w-full max-w-md bg-slate-800/80 backdrop-blur-lg shadow-2xl rounded-xl p-8 sm:p-10 space-y-6">
        <div className="text-center">
          {/* Using sky-500 for the icon color like in LoginPage */}
          <FilmReelIcon className="h-14 w-14 mx-auto text-sky-500 mb-3" />
          <h1 className="text-3xl font-bold text-white">CineSuggest</h1>
          <p className="text-slate-300 mt-1"> {/* Changed to slate-300 */}
            {registrationStage === 'register' ? 'Create your account' : 'Verify your account'}
          </p>
        </div>

        {displayError && (
          // Using rose color for errors like in LoginPage
          <div className="bg-rose-700/30 border border-rose-600 text-rose-300 px-4 py-3 rounded-lg text-sm" role="alert">
            <p>{displayError}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5"> {/* Adjusted space-y slightly */}
          {registrationStage === 'register' ? (
            <>
              <Input
                id="username-register"
                type="text"
                label="Username"
                placeholder="yourusername"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                icon={<UserIcon className="h-5 w-5 text-slate-400" />} // Added text-slate-400 to icon
                required
                disabled={isLoading}
                className="" // Ensure Input component handles its own focus/style
              />
              <Input
                id="email-register"
                type="email"
                label="Email Address"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                icon={<MailIcon className="h-5 w-5 text-slate-400" />} // Changed to MailIcon and added color
                required
                disabled={isLoading}
                className=""
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
                icon={<LockIcon className="h-5 w-5 text-slate-400" />} // Added text-slate-400
                required
                disabled={isLoading}
                error={passwordError} // Input component should display this error
                className=""
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
                icon={<LockIcon className="h-5 w-5 text-slate-400" />} // Added text-slate-400
                required
                disabled={isLoading}
                error={passwordError} // Input component should display this error
                className=""
              />
            </>
          ) : (
            <>
              <p className="text-sm text-center text-slate-300"> {/* Changed to slate-300 */}
                An OTP has been sent to <span className="font-semibold text-sky-400">{email}</span>. {/* Changed to sky-400 */}
              </p>
              <Input
                id="otp-input"
                type="text"
                label="Verification Code (OTP)"
                placeholder="XXXXXX"
                value={otp}
                onChange={(e) => {
                  setOtp(e.target.value);
                  if (otpError) setOtpError(null); // Clear OTP error on change
                }}
                icon={<LockIcon className="h-5 w-5 text-slate-400" />} // Added text-slate-400
                required
                disabled={isLoading || resendOtpIsLoading}
                error={otpError} // Input component should display this if not handled by the main error display
                className=""
              />
              <div className="text-center"> {/* Removed mt-2, handled by form's space-y */}
                <Button
                  type="button"
                  variant="link" // Ensure your Button component handles this variant style
                  onClick={handleResendOtp}
                  isLoading={resendOtpIsLoading}
                  disabled={resendOtpIsLoading || isLoading}
                  // Using sky-500 for links like in LoginPage
                  className="!text-sky-500 hover:!text-sky-400 hover:underline"
                >
                  {resendOtpIsLoading ? 'Resending OTP...' : 'Resend OTP'}
                </Button>
              </div>
            </>
          )}

          <Button
            type="submit"
            variant="primary" // Assuming this is your primary button style (e.g., sky blue)
            fullWidth
            isLoading={isLoading}
            disabled={isLoading || resendOtpIsLoading}
            className="" // Button component handles its own style
          >
            {isLoading
              ? (registrationStage === 'register' ? 'Registering...' : 'Verifying...')
              : (registrationStage === 'register' ? 'Create Account' : 'Verify & Register')}
          </Button>
        </form>

        <p className="text-sm text-center text-slate-400"> {/* Changed to slate-400 */}
          Already have an account?{' '}
          {/* Using sky-500 for links like in LoginPage */}
          <a href="/login" onClick={handleLoginClick} className="font-medium text-sky-500 hover:text-sky-400 hover:underline">
            Login here
          </a>
        </p>
      </div>
      
    </div>
  );
};

export default RegisterPage;