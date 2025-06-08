import React, { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import CardTheater from '../components/CardTheater';


const TheaterMovies = () => {
  const {
  data: theaterMovies,
  isLoading,
  isError, 
} =  useQuery({
  queryKey: ['theater-movies'],
  queryFn: async () => {
    const res = await fetch('http://localhost:8000/api/showtimes');
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ detail: "Network response was not ok" }));
      throw new Error(errorData.detail || "Failed to fetch theater movies");
    }
    return res.json();
  }
});
console.log("Theater Movies Data:", theaterMovies);
  return (
    <div className='py-16'>
        <div className='container mx-auto h-[470px]'>
          <h3 className='capitalize text-lg lg:text-xl font-semibold my-3'>Theater Movies</h3>
          <div className='grid grid-cols-[repeat(auto-fit,260px)] gap-6 justify-center lg:justify-start'>
              {
                theaterMovies?.map((movie,index)=>{
                  return(
                    <CardTheater data={movie} index={index} key={index+"theater"}  />
                  )
                })
              }
          </div>

        </div>
    </div>
  )
}

export default TheaterMovies