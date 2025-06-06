import React from "react";
import BannerHome from "../components/BannerHome";
import { useQuery } from "@tanstack/react-query";
import { FaAngleRight } from "react-icons/fa6";
import { FaAngleLeft } from "react-icons/fa6";
import { useEffect, useState } from "react";
import Card from "../components/Card";
import HorizontalScrollCard from "../components/HorizontalScrollCard";
import { useFetch } from "../hooks/useFetch";

const Home = () => {
  const {
    data: bannerData,
    isLoading: isBannerLoading,
    error: bannerError,
  } = useFetch("/movies/trending", "movies-trending");
  const {
    data: nowplayingData,
    isLoading: isLoadingNowPlaying,
    error: errorNowPlaying,
  } = useFetch("/movies", "movies-nowplaying");
  const {
    data: topRatedData,
    isLoading: isLoadingTopRated,
    error: errorTopRated, 
  } = useFetch("/movies/ratings", "movies-ratings");
  const {
    data: moviePopularData,
    isLoading: isMoviePopularLoading,
    error: errorPopularTVShow,
  } = useFetch("/movies/numVote", "movies-numVote");
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
  return (
    <div>
      <BannerHome bannerData={bannerData} />
      <HorizontalScrollCard data={bannerData} heading={"Trending"} trending={true}/>
      <HorizontalScrollCard data={nowplayingData} heading={"Now Playing"} />
      <HorizontalScrollCard data={topRatedData} heading={"Top Rated Movies"} />
      <HorizontalScrollCard data={moviePopularData} heading={"Most Popular Movies"} />
    </div>
  );
};

export default Home;
