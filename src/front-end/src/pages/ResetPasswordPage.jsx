import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, Link as RouterLink } from 'react-router-dom';
import Input from '../components/Input'; // Adjust path as necessary
import Button from '../components/Button'; // Adjust path as necessary
import LockIcon from '../components/icons/LockIcon'; // Adjust path as necessary
import MailIcon from '../components/icons/MailIcon'; // For username input

// Placeholder for KeyIcon or use your actual KeyIcon component
const PlaceholderKeyIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 5.25a3 3 0 0 1 3 3m3 0a6 6 0 0 1-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1 1 21.75 8.25Z" />
  </svg>
);

// FilmReelIcon (copied for consistency, or import from a shared location)
const FilmReelIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" {...props}>
    <path d="M18 3H6C4.346 3 3 4.346 3 6V18C3 19.654 4.346 21 6 21H18C19.654 21 21 19.654 21 18V6C21 4.346 19.654 3 18 3ZM7 17H5V15H7V17ZM7 13H5V11H7V13ZM7 9H5V7H7V9ZM15 17H9V7H15V17ZM19 17H17V15H19V17ZM19 13H17V11H19V13ZM19 9H17V7H19V9Z"/>
  </svg>
);

const ResetPasswordPage = () => {
  const [step, setStep] = useState(1); // 1: Enter username, 2: Enter code and new password
  const [usernameForReset, setUsernameForReset] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');

  const [isLoadingSendCode, setIsLoadingSendCode] = useState(false);
  const [isLoadingReset, setIsLoadingReset] = useState(false);

  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null); // For general success messages

  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Attempt to get username from navigation state passed from LoginPage
    if (location.state?.username) {
      setUsernameForReset(location.state.username);
    }
  }, [location.state]);

  const handleSendVerificationCode = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage(null);

    if (!usernameForReset) {
      setError('Username or Email is required.');
      return;
    }
    setIsLoadingSendCode(true);

    try {
      

      const response = await fetch(`http://localhost:8000/api/auth/send-verification-code?username=${encodeURIComponent(usernameForReset)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      const data = await response.json();

      if (response.ok && (!data.status || (data.status >= 200 && data.status < 300))) {
        setSuccessMessage(data.message || 'Verification code sent! Check your email.');
        setStep(2); // Move to step 2
      } else {
        setError(data.detail || data.message || 'Failed to send verification code.');
      }
    } catch (err) {
      console.error("Send verification code error:", err);
      setError('An error occurred while sending the code. Please try again.');
    }
    setIsLoadingSendCode(false);
  };


  const handleResetPasswordSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    // Keep successMessage from step 1 or clear it if you prefer
    // setSuccessMessage(null);

    if (!verificationCode) {
      setError('Verification code is required.');
      return;
    }
    if (newPassword !== confirmNewPassword) {
      setError('New passwords do not match.');
      return;
    }
    if (!newPassword) {
      setError('New password cannot be empty.');
      return;
    }

    setIsLoadingReset(true);

    try {
      const formData = new URLSearchParams();
      formData.append('code', verificationCode);
      formData.append('username', usernameForReset); // Username from step 1
      formData.append('new_password', newPassword);

      const response = await fetch(`http://localhost:8000/api/auth/reset-password?username=${encodeURIComponent(usernameForReset)}&code=${encodeURIComponent(verificationCode)}&new_password=${encodeURIComponent(newPassword)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();

      if (response.ok) {
        setSuccessMessage(data.message || 'Password has been reset successfully! You can now log in.');
        setStep(3); // Indicates success, form will be hidden
        // Optionally clear form or disable fields
        // setTimeout(() => navigate('/login'), 3000);
      } else {
        setError(data.detail || data.message || 'Failed to reset password. The code might be invalid, expired, or the username incorrect.');
      }
    } catch (err) {
      console.error("Reset password error:", err);
      setError('An error occurred while resetting your password. Please try again.');
    }
    setIsLoadingReset(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex flex-col justify-center items-center p-4 text-gray-100">
      <div className="w-full max-w-md bg-slate-800/80 backdrop-blur-lg shadow-2xl rounded-xl p-8 sm:p-6 space-y-6">
        <div className="text-center">
          <FilmReelIcon className="h-14 w-14 mx-auto text-sky-500 mb-2" />
          <h1 className="text-3xl font-bold text-white">Reset Your Password</h1>
        </div>

        {error && (
          <div className="bg-rose-700/30 border border-rose-600 text-rose-300 px-4 py-3 rounded-lg text-sm" role="alert">
            <p>{error}</p>
          </div>
        )}
        {successMessage && ( // Display success message, e.g., "Code sent" or "Password reset"
          <div className="bg-emerald-700/30 border border-emerald-600 text-emerald-300 px-4 py-3 rounded-lg text-sm" role="alert">
            <p>{successMessage}</p>
          </div>
        )}

        {step === 1 && (
          <form onSubmit={handleSendVerificationCode} className="space-y-4">
            <p className="text-slate-300 text-sm">
              Enter your username and we'll send you a code to reset your password.
            </p>
            <Input
              id="rp_username"
              type="text"
              label="Username"
              placeholder="username"
              value={usernameForReset}
              onChange={(e) => setUsernameForReset(e.target.value)}
              icon={<MailIcon className="h-5 w-5" />}
              required
              disabled={isLoadingSendCode}
            />
            <Button type="submit" variant="primary" fullWidth isLoading={isLoadingSendCode} disabled={isLoadingSendCode}>
              {isLoadingSendCode ? 'Sending Code...' : 'Send Verification Code'}
            </Button>
          </form>
        )}

        {step === 2 && (
          <form onSubmit={handleResetPasswordSubmit} className="space-y-4">
            <p className="text-slate-300 text-sm">
              A verification code has been sent to <span className="font-medium text-sky-400">{usernameForReset}</span>.
              Please enter the code and your new password below.
            </p>
            <Input
              id="verificationCode"
              type="text"
              label="Verification Code"
              placeholder="Enter code from email"
              value={verificationCode}
              onChange={(e) => setVerificationCode(e.target.value)}
              icon={<PlaceholderKeyIcon className="h-5 w-5" />}
              required
              disabled={isLoadingReset}
            />
            <Input
              id="newPassword"
              type="password"
              label="New Password"
              placeholder="••••••••"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              icon={<LockIcon className="h-5 w-5" />}
              required
              disabled={isLoadingReset}
            />
            <Input
              id="confirmNewPassword"
              type="password"
              label="Confirm New Password"
              placeholder="••••••••"
              value={confirmNewPassword}
              onChange={(e) => setConfirmNewPassword(e.target.value)}
              icon={<LockIcon className="h-5 w-5" />}
              required
              disabled={isLoadingReset}
            />
            <Button type="submit" variant="primary" fullWidth isLoading={isLoadingReset} disabled={isLoadingReset}>
              {isLoadingReset ? 'Resetting Password...' : 'Reset Password'}
            </Button>
          </form>
        )}
        
        {/* Always show "Back to Login" link, or conditionally if step is not 3 */}
        {/* If step is 3 (success), this link acts as "Proceed to Login" */}
        <div className="text-center mt-4">
          <RouterLink to="/login" className="text-sm text-sky-500 hover:text-sky-400 hover:underline">
            {step === 3 ? 'Proceed to Login' : 'Back to Login'}
          </RouterLink>
        </div>
        {step === 2 && ( // Option to go back to step 1 to resend code or change email
            <div className="text-center mt-2">
                 <button 
                    onClick={() => { setStep(1); setError(null); setSuccessMessage(null); setVerificationCode(''); setNewPassword(''); setConfirmNewPassword(''); }}
                    className="text-xs text-slate-400 hover:text-slate-300 hover:underline"
                >
                    Resend code or use different email?
                </button>
            </div>
        )}

      </div>
      <footer className="absolute bottom-4 text-center text-xs text-slate-500 w-full">
        © {new Date().getFullYear()} CineSuggest. All rights reserved.
      </footer>
    </div>
  );
};

export default ResetPasswordPage;