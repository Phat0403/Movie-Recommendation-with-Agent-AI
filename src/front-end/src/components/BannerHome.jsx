import React from "react";
import { useQuery } from "@tanstack/react-query";

const BannerHome = () => {
  const {
    data: bannerData = [],
    isLoading,
    error,
  } = useQuery({
    queryKey: ["movies"],
    queryFn: () =>
      fetch("http://localhost:8000/api/movies").then((res) => {
        if (!res.ok) {
          throw new Error("Network response was not ok");
        }
        return res.json();
      }),
  });
  console.log(bannerData);
  return (
    <section className="w-full h-full">
      <div className="flex min-h-full max-h-[95hv] overflow-hidden">
        {bannerData.map((data, index) => {
          return (
            <div className="min-w-full min-h-[450px] lg:min-h-full overflow-hidden relative">
              <div className="w-full h-full">
                <img
                  src={data.backdropPath}
                  className="w-full h-screen object-cover"
                />
              </div>
              {/*Button next and previous */}
            <div>
                
                </div>




              <div className="absolute top-0 w-full h-full bg-gradient-to-t from-neutral-900 to-transparent"></div>
              <div className="container mx-auto">
                <div className="w-full absolute bottom-0 max-w-md px-3">
                <h2 className="font-bold text-2xl lg:text-4xl text-white drop-shadow-2xl">
                  {data.primaryTitle}
                </h2>
                <p className="text-ellipsis line-clamp-3 my-2 ">
                  {data.description}
                </p>
                <div className="flex items-center gap-4">
                  <p>Rating : {data.rating}+</p>
                  <span>|</span>
                  <p>Votes : {data.numVotes}</p>
                </div>
                <button  onClick={() => alert('Clicked!')} className="bg-white px-4 py-2 rounded font-bold text-black mt-4 cursor-pointer hover:bg-gradient-to-l from-red-700 to-orange-500 shaow-md transition-all hover:scale-105" >
                  Play Now
                </button>
              </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default BannerHome;
