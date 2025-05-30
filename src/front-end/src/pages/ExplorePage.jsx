import React, { useEffect, useState }  from 'react'
import { useQuery } from '@tanstack/react-query'
import Card from '../components/Card'
import { useNavigate, useLocation } from 'react-router-dom'
import { CalendarIcon, GENRES, TagIcon, YEARS, FilterIcon } from '../components/constants';

const PAGE_SIZE = 20; // Number of movies per page

const ChevronLeftIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
  </svg>
);

const ChevronRightIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
  </svg>
);

const ExplorePage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const currentPage = Number(location?.search?.slice(6) || 0);
  const [selectedYear, setSelectedYear] = useState(0);
  const [selectedGenre, setSelectedGenre] = useState('all');
  const [selectedSort, setSelectedSort] = useState(0); 
   // Initialize with page from URL or default to 0
  console.log("Current Page:", currentPage);
  const {
    data: movies, // Rename data to movies for clarity, default to empty array
    isLoading,
    isError,
    error,
    isPreviousData, // Useful for UI state while fetching next page
  } = useQuery({
    queryKey: ['explore', currentPage, selectedYear, selectedGenre, selectedSort], // Query key depends on the current page
    queryFn: async () => {
      // Truyền các tham số vào URL nếu khác rỗng
      const res = await fetch(`http://localhost:8000/api/movies/explore?page=${currentPage}&size=${PAGE_SIZE}&year=${selectedYear}&genre=${selectedGenre}&sort=${selectedSort}`);
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({ detail: "Network response was not ok" }));
        throw new Error(errorData.detail || "Failed to fetch movies");
      }
      return res.json(); // Backend returns an array of movies
    },
    keepPreviousData: true, // Keep showing old data while fetching new
    // staleTime: 5 * 60 * 1000, // Optional: Data fresh for 5 minutes
  });

  const handleNextPage = () => {
    // Only increment if not currently fetching new data for a previous page state,
    // and if there's likely more data (current page was full)
    if (!isPreviousData && movies && movies.length === PAGE_SIZE) {
      navigate(`/explore?page=${currentPage+1}`); // Update URL to reflect new page
    }
  };

  const handlePrevPage = () => {
    navigate(`/explore?page=${Math.max(0, currentPage - 1)}`); // Update URL to reflect new page
  };

  const renderPaginationControls = () => (
    <div className="flex justify-between items-center my-8 px-4 py-3 bg-neutral-800 rounded-lg shadow-lg">
      <button
        onClick={handlePrevPage}
        disabled={currentPage === 0 || isPreviousData}
        className="flex items-center gap-2 bg-sky-600 hover:bg-sky-700 text-white font-semibold py-2 px-4 rounded-md transition-colors duration-150 disabled:opacity-60 disabled:cursor-not-allowed disabled:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-opacity-75 cursor-pointer"
      >
        <ChevronLeftIcon />
        Previous
      </button>
      
      <div className="text-center">
        <span className="text-md text-neutral-300">
          Page <span className="font-bold text-sky-400 text-lg">{currentPage}</span>
        </span>
        {movies && movies.length < PAGE_SIZE && movies.length > 0 && !isPreviousData && (
          <span className="block text-xs text-neutral-400 mt-1">(End of results)</span>
        )}
      </div>

      <button
        onClick={handleNextPage}
        disabled={isPreviousData || !movies || movies.length < PAGE_SIZE}
        className="flex items-center gap-2 bg-sky-600 hover:bg-sky-700 text-white font-semibold py-2 px-4 rounded-md transition-colors duration-150 disabled:opacity-60 disabled:cursor-not-allowed disabled:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-opacity-75 cursor-pointer"
      >
        Next
        <ChevronRightIcon />
      </button>
    </div>
  );
  const handleYearChange = (e) => {
    const year = e.target.value;
    setSelectedYear(year);
  }
  const handleGenreChange = (e) => {
    const genre = e.target.value;
    setSelectedGenre(genre);
  }
  const handleSortChange = (e) => {
    const sort = e.target.value;
    setSelectedSort(sort);
  }
  const renderFilters = () => (
    <div className="mb-8 p-6 bg-neutral-800 rounded-lg shadow-xl">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <label htmlFor="year-filter" className="flex items-center text-sm font-medium text-neutral-300 mb-1">
            <CalendarIcon />
            Year
          </label>
          <select
            id="year-filter"
            value={selectedYear}
            onChange={handleYearChange}
            className="w-full p-2.5 bg-neutral-700 border border-neutral-600 text-neutral-200 rounded-md shadow-sm focus:ring-sky-500 focus:border-sky-500 transition-colors"
          >
            <option value="0">All Years</option>
            {YEARS.map(year => (
              <option key={year} value={year.toString()}>{year}</option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="genre-filter" className="flex items-center text-sm font-medium text-neutral-300 mb-1">
            <TagIcon />
            Genre
          </label>
          <select
            id="genre-filter"
            value={selectedGenre}
            onChange={handleGenreChange}
            className="w-full p-2.5 bg-neutral-700 border border-neutral-600 text-neutral-200 rounded-md shadow-sm focus:ring-sky-500 focus:border-sky-500 transition-colors"
          >
            <option value="">All Genres</option>
            {GENRES.map(genre => (
              <option key={genre.id.toString()} value={genre.id.toString()}>{genre.name}</option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="rating-filter" className="flex items-center text-sm font-medium text-neutral-300 mb-1">
            <FilterIcon />
            Sort by Rating
          </label>
          <select
            id="rating-filter"
            value={selectedSort}
            onChange={handleSortChange}
            className="w-full p-2.5 bg-neutral-700 border border-neutral-600 text-neutral-200 rounded-md shadow-sm focus:ring-sky-500 focus:border-sky-500 transition-colors"
          >
            <option value="0">None</option>
            <option value="1">Ascending</option>
            <option value="-1">Descending</option>

          </select>
        </div>
      </div>
    </div>
  );
 
  return (
    <div className="py-16">
      <div className="container mx-auto ">
        <h3 className="capitalize text-lg lg:text-xl font-semibold my-3">
          Explore Movies
        </h3>
        {renderFilters()}

        {isLoading && (
          <div className="flex justify-center items-center h-64">
            <p className="text-xl text-neutral-400">Loading movies...</p>
            {/* You can add a spinner here */}
          </div>
        )}

        {isError && (
          <div className="flex justify-center items-center h-64">
            <p className="text-xl text-red-500 text-center">
              Error: {error?.message || 'Could not fetch movies.'}
            </p>
          </div>
        )}

        {!isLoading && !isError && movies && movies.length === 0 && (
          <div className="flex justify-center items-center h-64">
            <p className="text-xl text-neutral-400">No movies found for this page.</p>
          </div>
        )}

        {!isLoading && !isError && movies && movies.length > 0 && (
          <div className='grid grid-cols-[repeat(auto-fit,260px)] gap-6 justify-center lg:justify-start'>
              {
                movies.map((movie,index)=>{
                  return(
                    <Card data={movie} key={movie.id+"explore"} trending={false} />
                  )
                })
              }
          </div>
        )}

        {/* Optional: Render pagination controls at the bottom as well if the list is long */}
        {!isLoading && !isError && movies && movies.length > 0 && renderPaginationControls()}
      </div>
    </div>
  );
};

export default ExplorePage;