
import React from 'react';

const Input = ({ id, label, icon, error, className, ...props }) => {
  return (
    <div className="w-full">
      {label && (
        <label htmlFor={id} className="block text-sm font-medium text-slate-300 mb-1.5">
          {label}
        </label>
      )}
      <div className="relative rounded-lg shadow-sm">
        {icon && (
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
            <span className="text-slate-500 sm:text-sm">{icon}</span>
          </div>
        )}
        <input
          id={id}
          {...props}
          className={`
            block w-full px-3 py-2.5 border
            ${icon ? 'pl-10' : 'px-3.5'}
            ${error ? 'border-rose-500 text-rose-400 placeholder-rose-400/70 focus:ring-rose-500 focus:border-rose-500' : 'border-slate-600 focus:ring-sky-500 focus:border-sky-500'}
            bg-slate-700/50 text-slate-100 placeholder-slate-500 
            rounded-lg focus:outline-none sm:text-sm transition duration-150 ease-in-out
            disabled:opacity-70 disabled:cursor-not-allowed
            ${className || ''}
          `}
        />
      </div>
      {error && <p className="mt-1.5 text-xs text-rose-400">{error}</p>}
    </div>
  );
};

export default Input;