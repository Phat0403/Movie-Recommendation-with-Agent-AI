import React, { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import Card from '../components/Card'
const SearchPage = () => {
  const location = useLocation()
  const [page,setPage] = useState(1)
  const navigate = useNavigate()

  const query = location?.search?.slice(3)

  const {
    data = [],
    isLoading,
    error,
  } = useQuery({
    queryKey: ['search', query],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/movies/search/by-title?title='+query);
      if (!res.ok) {
        throw new Error("Network response was not ok");
      }
      return res.json();
    },
  });

  const handleScroll = ()=>{
    if((window.innerHeight + window.scrollY ) >= document.body.offsetHeight){
      setPage(preve => preve + 1)
    }
  }


  useEffect(()=>{
    window.addEventListener('scroll',handleScroll)
},[])

  return (
    <div className='py-16'>

        <div className='lg:hidden my-2 mx-1 sticky top-[70px] z-30'>
            <input 
              type='text'
              placeholder='Search here...'
              onChange={(e)=> navigate(`/search?q=${e.target.value}`)}
              value={query?.split("%20")?.join(" ")}
              className='px-4 py-1 text-lg w-full bg-white rounded-full text-neutral-900 '
            />
        </div>
        <div className='container mx-auto'>
          <h3 className='capitalize text-lg lg:text-xl font-semibold my-3'>Search Results</h3>

          <div className='grid grid-cols-[repeat(auto-fit,260px)] gap-6 justify-center lg:justify-start'>
              {
                data.map((searchData,index)=>{
                  return(
                    <Card data={searchData} key={searchData.id+"search"} trending={false} />
                  )
                })
              }
          </div>

        </div>
    </div>
  )
}

export default SearchPage