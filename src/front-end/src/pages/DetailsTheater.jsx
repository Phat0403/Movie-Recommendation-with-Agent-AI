import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import Divider from "../components/Divider";
import moment from "moment";
import VideoPlay from "../components/VideoPlay";
const StrToArray = (str) => {
  try {
    const newStr = str.split(",").map((item) => item.trim());
    return newStr;
  } catch (e) {
    console.error("Invalid format", e);
    return [];
  }
};

const DetailsTheater = () => {
  const { id } = useParams();
  const {
    data: theaterMovie,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["theater-movie", id],
    queryFn: async () => {
      const res = await fetch(`http://localhost:8000/api/showtimes/${id}`);
      if (!res.ok) {
        const errorData = await res
          .json()
          .catch(() => ({ detail: "Network response was not ok" }));
        throw new Error(
          errorData.detail || "Failed to fetch theater movie details"
        );
      }
      return res.json();
    },
  });
  const genres = StrToArray(theaterMovie?.genres);
  const [playVideo, setPlayVideo] = useState(false);
  const [playVideoId, setPlayVideoId] = useState("");

  const handlePlayVideo = (url) => {
    setPlayVideoId(url);
    setPlayVideo(true);
  };

  return (
    <div>
      <div className="w-full h-[280px] relative hidden lg:block">
        <div className="w-full h-full">
          <img
            src={theaterMovie?.backdrop_path}
            className="h-full w-full object-cover"
          />
        </div>
        <div className="absolute w-full h-full top-0 bg-gradient-to-t from-neutral-900/90 to-transparent"></div>
      </div>

      <div className="container mx-auto px-3 py-16 lg:py-0 flex flex-col lg:flex-row gap-5 lg:gap-10 ">
        <div className="relative mx-auto lg:-mt-28 lg:mx-0 w-fit min-w-60">
          <img
            src={theaterMovie?.poster_path}
            className="h-80 w-60 object-cover rounded"
          />
          <button
            onClick={() => handlePlayVideo(theaterMovie?.trailer)}
            className="mt-3 w-full py-2 px-4 text-center bg-white text-black rounded font-bold text-lg hover:bg-neutral-500 hover:scale-105 transition-all cursor-pointer"
          >
            Play Now
          </button>
           <button
            onClick={() => window.open(theaterMovie?.link, "_blank")}
            className="mt-3 w-full py-2 px-4 text-center bg-red-500 text-black rounded font-bold text-lg hover:bg-gradient-to-l from-red-500 to-orange-500 hover:scale-105 transition-all cursor-pointer"
          >
            Book tickets
          </button>
        </div>

        <div>
          <h2 className="text-2xl lg:text-4xl font-bold text-white ">
            {theaterMovie?.name}
          </h2>
          <Divider />
          <div className="flex items-center gap-2">
            <p>Genres:</p>
            {genres?.map((genre, index, arr) => (
              <span key={index}>
                {genre}
                {index < arr.length - 1 && "  |  "}
              </span>
            ))}
          </div>
          <Divider />
          <p>Rated : {theaterMovie?.rating}+</p>
          <Divider />
          <p>Duration : {theaterMovie?.duration}</p>
          <Divider />
          <p>Language : {theaterMovie?.language}</p>

          <Divider />

          <div>
            <h3 className="text-xl font-bold text-white mb-1">Overview</h3>
            <p>{theaterMovie?.description}</p>

            <Divider />
            <div className="flex items-center gap-3 my-3 text-center">
              <p>Staus : Released</p>
              <span>|</span>
              <p>
                Release Date :{" "}
                {moment(theaterMovie?.release_date).format("MMMM Do YYYY")}
              </p>
            </div>

            <Divider />
          </div>

          <div>
            <p>
              <span className="text-white">Director</span> :{" "}
              {theaterMovie?.director || "N/A"}
            </p>
          </div>

          <Divider />
          <div className="flex items-center gap-2">
            Actor: {theaterMovie?.actors}
          </div>
          <Divider />

        </div>
      </div>

      {/* <div>
        <HorizontalScollCard
          data={similarData}
          heading={"Similar " + params?.explore}
          media_type={params?.explore}
        />
        <HorizontalScollCard
          data={recommendationData}
          heading={"Recommendation " + params?.explore}
          media_type={params?.explore}
        />
      </div> */}

      {playVideo && (
        <VideoPlay
          close={() => setPlayVideo(false)}
          url={theaterMovie?.trailer}
        />
      )}
    </div>
  );
};

export default DetailsTheater;
