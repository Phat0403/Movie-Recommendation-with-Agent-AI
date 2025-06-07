import React, { useState } from 'react';
import { useParams } from "react-router-dom";
import { useFetchDetails } from "../hooks/useFetchDetails";
import Divider from "../components/Divider";
import moment from "moment";
import VideoPlay from '../components/VideoPlay';
import { useFetchTheMovieDb } from '../hooks/useFetchCast';
import CastList from '../components/CastList';
import CommentSection from '../components/CommentSection';
import { useAuth } from '../hooks/useAuth';
import { addToMyList } from '../hooks/myListApi';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast'; // <-- 1. Import toast

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
}

const DetailsPage = () => {
  const { id } = useParams();
  const { currentUser, loadingAuth } = useAuth();
  const queryClient = useQueryClient(); // <-- Lấy query client

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

  // <-- 2. Thiết lập useMutation
  const addToListMutation = useMutation({
    mutationFn: addToMyList, // Hàm thực hiện hành động
    onSuccess: () => {
      // Khi thành công
      toast.success("Added to your list successfully!");
      // Tùy chọn: Vô hiệu hóa và fetch lại query của "my-list" nếu có
      // queryClient.invalidateQueries({ queryKey: ['my-list'] });
    },
    onError: (error) => {
      // Khi có lỗi
      console.error("Error adding to list:", error);
      // Bạn có thể tùy chỉnh thông báo lỗi dựa trên `error` trả về từ API
      const errorMessage = error.response?.data?.message || "Failed to add to your list. Please try again.";
      toast.error(errorMessage);
    },
  });


  const [playVideo, setPlayVideo] = useState(false);
  const [playVideoId, setPlayVideoId] = useState("");

  if (detailsLoading || castLoading || loadingAuth) {
    return <div>Loading...</div>;
  }
  // Nếu có lỗi fetch data, bạn nên hiển thị thông báo
  if (detailsError || castError) {
    return <div>Error loading movie details.</div>;
  }

  const genres = StrToArray(detailsData.genres);

  const handlePlayVideo = (url) => {
    setPlayVideoId(url);
    setPlayVideo(true);
  };

  const writer = castData?.crew?.filter(el => el?.job === "Writer")?.map(el => el?.name)?.join(", ");

  // <-- 3. Cập nhật handleAddToList để sử dụng mutation
  const handleAddToList = () => {
    if (!currentUser) {
      toast.error("Please login to add to your list"); // Thay thế alert
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
          {/* 4. Cập nhật nút Add to MyList */}
          <button
            onClick={handleAddToList}
            disabled={addToListMutation.isPending} // Vô hiệu hóa nút khi đang gửi request
            className="mt-3 w-full py-2 px-4 text-center bg-white text-black rounded font-bold text-lg hover:bg-gradient-to-l from-red-500 to-orange-500 hover:scale-105 transition-all cursor-pointer disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {addToListMutation.isPending ? 'Adding...' : 'Add to MyList'}
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
          <Divider />
          {!loadingAuth && (
           <CommentSection movieId={id} currentUser={currentUser} />
          )}
        </div>
      </div>

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