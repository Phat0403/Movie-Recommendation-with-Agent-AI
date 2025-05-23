import React from 'react'
import moment from 'moment'
const Card = ({data, trending, index}) => {
  return (
    <div className='w-full min-w-[260px] max-w-[260px] h-80 overflow-hidden rounded relative block transition-all hover:scale-105 cursor-pointer'>
        <img src={data.posterPath} />
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
                <p className='bg-black px-1 rounded-full text-xs text-white'>Rating: {data.rating}</p>
            </div>
        </div>


    </div>
  )
}

export default Card