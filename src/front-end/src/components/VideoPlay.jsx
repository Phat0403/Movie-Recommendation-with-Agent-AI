import React from "react";
import { IoClose } from "react-icons/io5";
const VideoPlay = ({ close, url }) => {
    const extractVideoId = (url) => {
    const urlObj = new URL(url);
    return urlObj.searchParams.get("v");
  };

  const videoId = extractVideoId(url);
    const embedUrl = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
  console.log(url);
  return (
    <div onClick={close} className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center">
      <div onClick={(e) => e.stopPropagation()} className="relative w-[90%] max-w-4xl aspect-video">
        <iframe
          src={embedUrl}
          title="YouTube Video"
          className="w-full h-full rounded"
          frameBorder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        ></iframe>

        {/* Close button */}
        <button
          onClick={close}
          className="absolute -top-3 -right-3 text-white text-2xl font-bold rounded-full cursor-pointer hover:bg-red-500 w-8 h-8 "
        >
          ✕
        </button>
      </div>
    </div>
  );
};

export default VideoPlay;
