import React, { useEffect, useState } from "react";
import { useParams, useLocation } from "react-router-dom";
import { useFetchDetails } from "../hooks/useFetchDetails";
import Divider from "../components/Divider";
import moment from "moment";
import VideoPlay from "../components/VideoPlay";
import { useFetchTheMovieDb } from "../hooks/useFetchCast";
import CastList from "../components/CastList";
import CommentSection from "../components/CommentSection";
import { useAuth } from "../hooks/useAuth";
import { addToMyList } from "../hooks/myListApi";
import { useMutation, useQueryClient, useQueries } from "@tanstack/react-query";
import { toast } from "react-hot-toast";
import { useFetch } from "../hooks/useFetch"; // This is okay for single fetches at the top level
import HorizontalScrollCard from "../components/HorizontalScrollCard";

const formatMinutesToHours = (minutes) => {
  const hrs = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return `${hrs}h ${mins}m`;
};

const StrToArray = (str) => {
  try {
    if (typeof str !== "string") return [];
    return JSON.parse(str.replace(/'/g, '"'));
  } catch (e) {
    console.error("Invalid format", e);
    return [];
  }
};

// Define your actual fetcher function here.
// This function should NOT be a hook. It's just a regular async function.
// It should match what your `useFetch` hook does internally.
const apiFetcher = async (endpoint) => {
  // Replace this with your actual API URL and fetching logic (e.g., using axios)
  const response = await fetch(`http://localhost:8000/api/movies/by-genre?genre=${endpoint}`);

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  return response.json();
};

const DetailsPage = () => {
  const { id } = useParams();
  const location = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [id, location.pathname]); // Added location.pathname to re-scroll on same component but different page

  const { currentUser, loadingAuth } = useAuth();
  const queryClient = useQueryClient();

  const {
    data: detailsData,
    isLoading: detailsLoading,
    error: detailsError,
  } = useFetchDetails(`/movie/${id}`, "details-movie");

  const {
    data: castData,
    isLoading: castLoading,
    error: castError,
  } = useFetchTheMovieDb(`/movie/${id}/credits?language=en-US`, "cast-movie");
console.log("Cast Data:", castData);
  const {
    data: recommendationsData,
    isLoading: recommendationsLoading,
    error: recommendationsError,
  } = useFetch(`/movies/recommend/${id}`, "recommendations-movie");

  const addToListMutation = useMutation({
    mutationFn: addToMyList,
    onSuccess: () => {
      toast.success("Added to your list successfully!");
      queryClient.invalidateQueries({ queryKey: ["my-list"] }); // It's good practice to invalidate the list
    },
    onError: (error) => {
      console.error("Error adding to list:", error);
      const errorMessage =
        error.response?.data?.message ||
        "Failed to add to your list. Item may already be in the list.";
      toast.error(errorMessage);
    },
  });

  const [playVideo, setPlayVideo] = useState(false);
  const [playVideoId, setPlayVideoId] = useState("");

  const genres = detailsData ? StrToArray(detailsData.genres) : [];
console.log("Genres:", genres);
  // ***** CORRECTED useQueries HOOK *****
  const movieByGenreQueries = useQueries({
    queries: genres
      .filter((g) => g && g.trim()) // Filter out any empty/null genres
      .map((genre) => ({
        queryKey: ["movie-by-genre", genre],
        // Use a regular async fetcher function here, NOT a hook.
        queryFn: () => apiFetcher(genre),
        enabled: !!genre && genre.length > 0, // This is correct, it enables the query only when genre exists
      })),
  });
  
  // Extract data from the queries
  const movieByGenreData = movieByGenreQueries
    .map((query) => query.data)
    .filter((data) => data && data.length > 0);
  console.log("Movie by Genre Data:", movieByGenreData);
  if (detailsLoading || castLoading || loadingAuth) {
    return <div>Loading...</div>;
  }

  if (detailsError || castError) {
    return <div>Error loading movie details.</div>;
  }

  const handlePlayVideo = () => {
    setPlayVideoId(detailsData.trailerPath);
    setPlayVideo(true);
  };

  const writer = castData?.crew
    ?.filter((el) => el?.job === "Writer")
    ?.map((el) => el?.name)
    ?.join(", ");

  const handleAddToList = () => {
    if (!currentUser) {
      toast.error("Please login to add to your list");
      return;
    }
    addToListMutation.mutate({
      movieId: id,
      token: currentUser?.token,
    });
  };

  return (
    <div>
      <div className="w-full h-[280px] relative hidden lg:block">
        <div className="w-full h-full">
          <img
            src={detailsData.backdropPath}
            alt={detailsData.primaryTitle}
            className="h-full w-full object-cover"
          />
        </div>
        <div className="absolute w-full h-full top-0 bg-gradient-to-t from-neutral-900/90 to-transparent"></div>
      </div>

      <div className="container mx-auto px-3 py-16 lg:py-0 flex flex-col lg:flex-row gap-5 lg:gap-10 ">
        <div className="relative mx-auto lg:-mt-28 lg:mx-0 w-fit min-w-60">
          <img
            src={detailsData.posterPath}
            alt={detailsData.primaryTitle}
            className="h-80 w-60 object-cover rounded"
          />
          <button
            onClick={handlePlayVideo}
            className="mt-3 w-full py-2 px-4 text-center bg-white text-black rounded font-bold text-lg hover:bg-gradient-to-l from-red-500 to-orange-500 hover:scale-105 transition-all cursor-pointer"
          >
            Play Now
          </button>
          <button
            onClick={handleAddToList}
            disabled={addToListMutation.isPending}
            className="mt-3 w-full py-2 px-4 text-center bg-white text-black rounded font-bold text-lg hover:bg-gradient-to-l from-red-500 to-orange-500 hover:scale-105 transition-all cursor-pointer disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {addToListMutation.isPending ? "Adding..." : "Add to MyList"}
          </button>
        </div>

        <div>
          <h2 className="text-2xl lg:text-4xl font-bold text-white ">
            {detailsData.primaryTitle}
          </h2>
          <Divider />
          <div className="flex items-center gap-2 flex-wrap">
            <p>Genres:</p>
            {genres
              .filter((genre) => genre && genre.trim())
              .map((genre, index, arr) => (
                <span key={index}>
                  {genre}
                  {index < arr.length - 1 && "  |  "}
                </span>
              ))}
          </div>
          <Divider />

          <div className="flex items-center gap-3">
            <p>Rating : {Number(detailsData.rating).toFixed(1)}+</p>
            <span>|</span>
            <p>View : {Number(detailsData.numVotes)}</p>
            <span>|</span>
            <p>Duration : {formatMinutesToHours(detailsData.runtimeMinutes)}</p>
          </div>

          <Divider />

          <div>
            <h3 className="text-xl font-bold text-white mb-1">Overview</h3>
            <p>{detailsData.description}</p>

            <Divider />
            <div className="flex items-center gap-3 my-3 text-center">
              <p>Staus : Released</p>
              <span>|</span>
              <p>
                Release Date :{" "}
                {moment(detailsData.release_date).format("MMMM Do YYYY")}
              </p>
            </div>

            <Divider />
          </div>

          <div>
            <p>
              <span className="text-white">Director</span> :{" "}
              {castData?.crew?.[0]?.name}
            </p>

            <Divider />

            <p>
              <span className="text-white">Writer : {writer}</span>
            </p>
          </div>

          <Divider />

          <CastList castData={castData} />
          {!loadingAuth && (
            <CommentSection movieId={id} currentUser={currentUser} />
          )}
          <Divider />
        </div>
      </div>
      <HorizontalScrollCard
        data={recommendationsData}
        heading={"Recommendations"}
        isLoading={recommendationsLoading}
        media_type={"movie"}
      />
      {movieByGenreData.map((data, index) => (
        <HorizontalScrollCard
          data={data}
          heading={`More in ${genres[index]}`
        }   
        key={index}
        />
      ))}
      {playVideo && (
        <VideoPlay
          close={() => setPlayVideo(false)}
          url={detailsData.trailerPath}
        />
      )}
    </div>
  );
};

export default DetailsPage;