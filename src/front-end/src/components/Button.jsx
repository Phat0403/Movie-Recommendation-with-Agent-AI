
import React from 'react';

const Button = ({
  children,
  variant = 'primary',
  fullWidth = false,
  isLoading = false,
  icon,
  className,
  ...props
}) => {
  const baseStyles = "flex items-center justify-center px-4 py-2.5 border border-transparent text-sm font-semibold rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-900 transition-all duration-150 ease-in-out disabled:opacity-60 disabled:cursor-not-allowed";
  
  let variantStyles = '';
  switch (variant) {
    case 'primary':
      variantStyles = 'bg-sky-600 text-white hover:bg-sky-700 focus:ring-sky-500 disabled:hover:bg-sky-600';
      break;
    case 'secondary':
      variantStyles = 'bg-slate-600 text-slate-100 hover:bg-slate-500 focus:ring-slate-400 disabled:hover:bg-slate-600';
      break;
    case 'google':
      variantStyles = 'bg-white text-slate-700 hover:bg-slate-100 border-slate-300 shadow-sm focus:ring-sky-500 disabled:hover:bg-white';
      break;
    case 'link':
      // For link variant, specific styling is applied.
      return (
         <button
          {...props}
          className={`
            text-sky-500 hover:text-sky-400 p-0 shadow-none border-none bg-transparent focus:ring-sky-500
            inline font-medium text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-900 rounded
            disabled:opacity-60 disabled:cursor-not-allowed
            ${isLoading ? 'cursor-wait' : ''}
            ${className || ''}
          `}
          disabled={props.disabled || isLoading}
        >
           {children}
        </button>
      );
  }

  return (
    <button
      {...props}
      className={`
        ${baseStyles}
        ${variantStyles}
        ${fullWidth ? 'w-full' : ''}
        ${isLoading ? 'cursor-wait' : ''}
        ${className || ''}
      `}
      disabled={props.disabled || isLoading}
    >
      {isLoading ? (
        <svg className="animate-spin h-5 w-5 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      ) : (
        icon && <span className={`mr-2 ${children ? '' : 'mx-auto'}`}>{icon}</span> 
      )}
      {children}
    </button>
  );
};

export default Button;