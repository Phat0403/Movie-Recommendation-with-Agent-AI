import React from 'react';
import moment from 'moment';
import { Link } from 'react-router-dom';
import { FaTrashAlt } from "react-icons/fa";

const Card = ({ data, trending, index, onRemove = false, isRemoving = false }) => {

  const handleRemoveClick = (e) => {
    e.preventDefault();
    e.stopPropagation();

    if (onRemove) {
      onRemove(data.tconst);
    }
  };

  return (
    <div className='w-full min-w-[260px] max-w-[260px] h-80 rounded relative group transition-all hover:scale-105'>
      
      <Link to={"/"+'movie/'+data.tconst} className='w-full h-full block overflow-hidden rounded cursor-pointer'>
        <img src={data.posterPath || 'https://via.placeholder.com/260x320?text=No+Image'} alt={data.primaryTitle} className='w-full h-full object-cover' />
        
        <div className='absolute top-4'>
            {trending && (
                <div className=' py-1 px-4 backdrop-blur-3xl rounded-r-full bg-black/60 overflow-hidden'>
                    #{index} Trending
                </div>
            )}
        </div>

        <div className='absolute bottom-0 h-16 backdrop-blur-3xl w-full bg-black/60 p-2'>
            <h2 className='text-ellipsis line-clamp-1 text-lg font-semibold'>{data.primaryTitle}</h2>
            <div className='text-sm text-neutral-400 flex justify-between items-center'>
                <p>{moment(data.release_date).format('MMMM Do YYYY')}</p>
                <p className='bg-black px-1 rounded-full text-xs text-white'>Rating: {data.averageRating || data.rating || 'N/A'}</p>
            </div>
        </div>
      </Link>

      {onRemove && (
        <button
          onClick={handleRemoveClick}
          disabled={isRemoving}
          className="absolute top-2 right-2 z-10 bg-red-600 cursor-pointer hover:bg-red-700 text-white p-2 rounded-full transition-opacity duration-300 opacity-0 group-hover:opacity-100 disabled:opacity-50 disabled:cursor-not-allowed"
          aria-label={`Remove ${data.primaryTitle} from my list`}
        >
          {isRemoving ? (
            <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : (
            <FaTrashAlt size={16} />
          )}
        </button>
      )}

    </div>
  );
}

export default Card;