import React, { useState } from 'react'
import { useParams } from "react-router-dom";
import { useFetchDetails } from "../hooks/useFetchDetails";
import Divider from "../components/Divider";
import moment from "moment";
import VideoPlay from '../components/VideoPlay';
import { useFetchTheMovieDb } from '../hooks/useFetchCast';
import CastList from '../components/CastList';
const formatMinutesToHours = (minutes) => {
  const hrs = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return `${hrs}h ${mins}m`;
};
const StrToArray = (str) => {
  try {
    if (typeof str !== "string") return []; // kiểm tra str hợp lệ
    return JSON.parse(str.replace(/'/g, '"'));
  } catch (e) {
    console.error("Invalid format", e);
    return [];
  }
}

const DetailsPage = () => {
  const { id } = useParams();
  const {
    data: detailsData,
    isLoading: detailsLoading,
    error: detailsError,
  } = useFetchDetails(`/movie/${id}`, "details-movie");

  const {
    data: castData,
    isLoading: castLoading,
    error: castError,}
  = useFetchTheMovieDb(`/movie/${id}/credits?language=en-US`, "cast-movie");
  console.log(castData);
  const genres = StrToArray(detailsData.genres);
  const [playVideo, setPlayVideo] = useState(false);
  const [playVideoId, setPlayVideoId] = useState("");
  const handlePlayVideo = (url) => {
    setPlayVideoId(url);
    setPlayVideo(true);
  };
  const writer = castData?.crew?.filter(el => el?.job === "Writer")?.map(el => el?.name)?.join(", ")
  return (
    <div>
      <div className="w-full h-[280px] relative hidden lg:block">
        <div className="w-full h-full">
          <img
            src={detailsData.backdropPath}
            className="h-full w-full object-cover"
          />
        </div>
        <div className="absolute w-full h-full top-0 bg-gradient-to-t from-neutral-900/90 to-transparent"></div>
      </div>

      <div className="container mx-auto px-3 py-16 lg:py-0 flex flex-col lg:flex-row gap-5 lg:gap-10 ">
        <div className="relative mx-auto lg:-mt-28 lg:mx-0 w-fit min-w-60">
          <img
            src={detailsData.posterPath}
            className="h-80 w-60 object-cover rounded"
          />
          <button
            onClick={() => handlePlayVideo(detailsData.trailerPath)}
            className="mt-3 w-full py-2 px-4 text-center bg-white text-black rounded font-bold text-lg hover:bg-gradient-to-l from-red-500 to-orange-500 hover:scale-105 transition-all cursor-pointer"
          >
            Play Now
          </button>
        </div>

        <div>
          <h2 className="text-2xl lg:text-4xl font-bold text-white ">
            {detailsData.primaryTitle}
          </h2>
          <Divider />
          <div className="flex items-center gap-2">
            <p>Genres:</p>
            {genres
              .filter((genre) => genre && genre.trim()) // lọc bỏ genre rỗng
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
          url={detailsData.trailerPath}
        />
      )}
    </div>
  );
};

export default DetailsPage;
