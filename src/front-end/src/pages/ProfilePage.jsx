import React from "react";
import { useAuth } from "../hooks/useAuth";
import Card from "../components/Card";
import { removeFromMyList } from "../hooks/myListApi";
import { useQuery, useQueries, useMutation, useQueryClient } from "@tanstack/react-query";
import HorizontalScrollCard from "../components/HorizontalScrollCard";
// --- Icon components and API fetch functions remain the same ---

export const UserCircleIcon = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    strokeWidth={1.5}
    stroke="currentColor"
    {...props}
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
    />
  </svg>
);

export const HeartIcon = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    strokeWidth={1.5}
    stroke="currentColor"
    {...props}
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z"
    />
  </svg>
);

export const ChatBubbleLeftRightIcon = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    strokeWidth={1.5}
    stroke="currentColor"
    {...props}
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3.007-3.007c-1.334-.215-2.585-.59-3.728-.995a9.723 9.723 0 0 1-.504-16.096A18.726 18.726 0 0 1 20.25 8.511Zm-10.865-1.572c-3.483 0-6.33 2.503-6.33 5.625v2.859c0 .548.199 1.054.542 1.459l2.128 2.127V17.51a8.38 8.38 0 0 0 5.43-.981c2.315-.812 3.963-2.88 3.963-5.325 0-3.122-2.847-5.625-6.33-5.625Z"
    />
  </svg>
);

const fetchUserInfo = async (token) => {
    const response = await fetch("http://localhost:8000/api/user/user-info", {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
};

const fetchMovieDetails = async (movieId) => {
  const response = await fetch(`http://localhost:8000/api/movie/${movieId}`);
  if (!response.ok) throw new Error(`Failed to fetch movie details for ID: ${movieId}`);
  return response.json();
};

const fetchRecommendations = async (username, movieList) => {
    console.log("Fetching recommendations for user:", username, "with movie list:", movieList);
  const response = await fetch(`http://localhost:8000/api/movies/recommend-by-user/${username}?size=20`, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'accept': 'application/json' 
    },
    body: JSON.stringify({ movie_list: movieList }),
  });
  if (!response.ok) throw new Error('Failed to fetch recommendations');
  return response.json();
};

const ProfilePage = () => {
  // --- 1. ALL HOOKS ARE CALLED AT THE TOP LEVEL, IN THE SAME ORDER ---
  const { currentUser } = useAuth();
  const queryClient = useQueryClient();

  const { data: userData, isLoading: isUserLoading, error: userError } = useQuery({
      queryKey: ['userInfo', currentUser?.token],
      queryFn: () => fetchUserInfo(currentUser.token),
      enabled: !!currentUser?.token,
  });

  const allMovieIds = React.useMemo(() => {
    if (!userData) return [];
    const favoriteIds = userData.favorite_movies || [];
    const commentMovieIds = (userData.comments || []).map(commentObj => Object.keys(commentObj)[0]);
    return [...new Set([...favoriteIds, ...commentMovieIds])];
  }, [userData]);
  
  const movieDetailsQueries = useQueries({
    queries: allMovieIds.map((movieId) => ({
      queryKey: ["movie", movieId],
      queryFn: () => fetchMovieDetails(movieId),
      enabled: !!movieId,
    })),
  });

  const moviesMap = React.useMemo(() => {
      const map = new Map();
      movieDetailsQueries.forEach(query => {
          if (query.isSuccess && query.data) {
              const movieData = Array.isArray(query.data) ? query.data[0] : query.data;
              if (movieData && movieData.tconst) {
                map.set(String(movieData.tconst), movieData);
              }
          }
      });
      return map;
  }, [movieDetailsQueries]);
  
  // This derived list is now defined up here so the recommendations query can use it
  const favoriteMoviesList = React.useMemo(() => 
    (userData?.favorite_movies || [])
      .map(id => moviesMap.get(String(id)))
      .filter(Boolean),
    [userData, moviesMap]
  );
  // --- 2. MOVE THE RECOMMENDATIONS HOOK HERE, TO THE TOP LEVEL ---
  const { data: recommendationsList, isLoading: isRecommendationsLoading } = useQuery({
    // The query key includes the list of favorites, so it refetches if the list changes.
    queryKey: ['recommendations', userData?.favorite_movies], 
    queryFn: () => fetchRecommendations(currentUser.username, userData?.favorite_movies),
    // IMPORTANT: Only enable this query AFTER the favorite movies list has been populated.
    enabled: !!userData?.favorite_movies 
  });

  const removeMovieMutation = useMutation({
    mutationFn: removeFromMyList,
    onSuccess: () => {
      console.log("Movie removed! Invalidating userInfo query...");
      queryClient.invalidateQueries({ queryKey: ["userInfo", currentUser?.token] });
      // Invalidation of 'userInfo' will cause favoriteMoviesList to update,
      // which will then cause the 'recommendations' query to refetch automatically.
    },
    onError: (error) => {
      console.error("Failed to remove movie:", error);
      alert(error.message || "Could not remove the movie. Please try again.");
    }
  });

  // --- Helper Functions ---
  const getMovieById = (movieId) => moviesMap.get(String(movieId));

  const handleRemoveMovie = (movieId) => {
    if (!currentUser?.token) return;
    removeMovieMutation.mutate({ movieId, token: currentUser.token });
  };
 
  const onNavigateBack = () => console.log("Navigating back...");

  // --- Render Logic ---
  // The conditional returns now happen AFTER all hooks have been called.
  if (isUserLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-sky-500"></div>
        <p className="ml-4 text-lg text-gray-300">Loading Profile...</p>
      </div>
    );
  }

  if (userError) {
    return (
      <div className="text-center p-8 mt-20 bg-neutral-700 rounded-lg shadow-xl">
        <h2 className="text-2xl font-semibold text-red-400 mb-4">Error Loading Profile</h2>
        <p className="text-gray-300 mb-6">{userError.message}</p>
      </div>
    );
  }

  if (!userData) {
    return (
      <div className="text-center p-8 mt-20">
        <p className="text-lg text-gray-400">No user data found or not authenticated.</p>
      </div>
    );
  }

  return (
    <div className="mt-20 max-w-4xl mx-auto p-4 md:p-6 bg-neutral-800 text-gray-200 rounded-lg">
      <section className="mb-8 p-6 bg-neutral-700 rounded-xl shadow-xl flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-6">
        <UserCircleIcon className="w-24 h-24 text-sky-500 flex-shrink-0" />
        <div className="text-center sm:text-left">
          <h1 className="text-3xl font-bold text-white">{userData.username}</h1>
          <p className="text-md text-gray-400">{userData.email || "No email provided"}</p>
        </div>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-white mb-4 flex items-center">
          <HeartIcon className="w-7 h-7 mr-3 text-red-500" />
          My Favorite Movies
        </h2>
        {favoriteMoviesList.length > 0 ? (
          <div className="grid grid-cols-[repeat(auto-fit,260px)] gap-6 justify-center lg:justify-start">
            {favoriteMoviesList.map((movie, index) => {
              const isRemoving = 
                removeMovieMutation.isPending && 
                removeMovieMutation.variables?.movieId === movie.tconst;
              return (
                <Card 
                  data={movie}
                  key={movie.tconst + 'favourite' + index}
                  index={index + 1}
                  trending={false} 
                  onRemove={handleRemoveMovie}
                  isRemoving={isRemoving}
                />
              )
            })}
          </div>
        ) : (
          <p className="text-gray-400 italic">Add movies to your favorites to get recommendations!</p>
        )}
      </section>

      

      <section>
        <h2 className="text-2xl font-semibold text-white mb-4 flex items-center">
          <ChatBubbleLeftRightIcon className="w-7 h-7 mr-3 text-green-500" />
          My Comments
        </h2>
        {userData.comments && userData.comments.length > 0 ? (
          <ul className="space-y-4">
            {userData.comments.map((commentObj, index) => {
              const movieId = Object.keys(commentObj)[0];
              const commentText = commentObj[movieId];
              const movie = getMovieById(movieId);
              return (
                <li key={index} className="bg-neutral-700 p-4 rounded-lg shadow-lg">
                  <p className="text-sm text-gray-300">
                    On <span className="font-semibold text-sky-400">
                      {movie ? movie.primaryTitle : `Movie ID: ${movieId}`}
                    </span>: "{commentText.trim()}"
                  </p>
                </li>
              );
            })}
          </ul>
        ) : (
          <p className="text-gray-400 italic">No comments made yet.</p>
        )}
      </section>
      
      <HorizontalScrollCard
             data={recommendationsList}
             heading="Recommended Movies"
             trending={false}/>
    </div>
  );
};

export default ProfilePage;