import React from "react";
import moment from "moment";
import { Link } from "react-router-dom";
const CardTheater = ({ data, index }) => {
  return (
    <Link
      to={"/" + "theater-movie/" + index}
      className="w-full min-w-[260px] max-w-[260px] h-80 overflow-hidden rounded relative block transition-all hover:scale-105 cursor-pointer"
    >
      <img src={data.poster_path} />
      <div className="absolute top-4">
        <div className=" py-1 px-4 backdrop-blur-3xl rounded-r-full bg-black/60 overflow-hidden">
          New
        </div>
      </div>
      <div className="absolute bottom-0 h-16 backdrop-blur-3xl w-full bg-black/60 p-2">
        <h2 className="text-ellipsis line-clamp-1 text-lg font-semibold">
          {data.name}
        </h2>
        <div className="text-sm text-neutral-400 flex justify-between items-center">
      <p>{moment(data.release_date.trim(), "DD/MM/YYYY").format("MMMM Do YYYY")}</p>
        </div>
      </div>
    </Link>
  );
};

export default CardTheater;
