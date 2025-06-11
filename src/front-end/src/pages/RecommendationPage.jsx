import React from "react";
import { useLocation } from "react-router-dom";
import {
  useQuery,
  useQueries,
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";
import Card from "../components/Card";
const fetchMovieDetails = async (movieId) => {
  const response = await fetch(`http://localhost:8000/api/movie/${movieId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch movie details for ID: ${movieId}`);
  }
  return response.json();
};

const RecommendationPage = () => {
  const location = useLocation();
  const listID = location.state?.data || null; // Get listID from state or set to null if not available
  console.log("List ID:", listID); // Log the listID to verify it's being passed correctly
  const movieDetailsQueries = useQueries({
    queries: (listID || []).map((movieId) => ({
      queryKey: ["movie", movieId],
      queryFn: () => fetchMovieDetails(movieId),
      enabled: !!listID && listID.length > 0,
    })),
  });

  const isLoading = movieDetailsQueries.some((query) => query.isLoading);
  if (isLoading) return <div>Loading...</div>;
  const moviesList = movieDetailsQueries
    .filter((query) => query.isSuccess)
    .map((query) => query.data);
  console.log("Movies List:", moviesList); // Log the movies list to verify it's being fetched correctly
  return (
    <div className="py-16 h-full">
      <div className="container mx-auto">
       

        {moviesList.length > 0 ? (
          <div className="grid grid-cols-[repeat(auto-fit,260px)] gap-6 justify-center lg:justify-start">
            {moviesList.map((movie, index) => {
              // 7. Xác định xem phim này có đang trong quá trình xóa hay không
              return (
                <Card
                  key={movie[0].tconst || index}
                  data={movie[0]}
                  index={index}
                  trending={false}
                />
              );
            })}
          </div>
        ) : (
          <p>Your list is empty.</p>
        )}
      </div>
    </div>
  );
};

export default RecommendationPage;
