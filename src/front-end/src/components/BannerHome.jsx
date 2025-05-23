import React, { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { FaAngleRight } from "react-icons/fa6";
import { FaAngleLeft } from "react-icons/fa6";
import { useState } from "react";



const BannerHome = ({bannerData}) => {
  
  const [currentImage, setCurrentImage] = useState(0);
  console.log(bannerData);
  const handleNext = () => {
    // Logic to show the next banner
    if (currentImage < bannerData.length - 1) {
      setCurrentImage(currentImage + 1);
    } else {
      setCurrentImage(0);
    }
  }
  const handlePrevious = () => {
    // Logic to show the previous banner
    if (currentImage > 0) {
      setCurrentImage(currentImage - 1);
    } else {
      setCurrentImage(bannerData.length - 1);
    }
  }

useEffect(() => {
  const interval = setInterval(() => {
    if (currentImage < bannerData.length - 1) {
      handleNext();
    } else {
      setCurrentImage(0);
    }
  }, 5000); // Change image every 5 seconds
  return () => clearInterval(interval); // Cleanup the interval on component unmount
}
, [bannerData, currentImage]);

  return (
    <section className="w-full h-full">
      <div className="flex min-h-full max-h-[95hv] overflow-hidden">
        {bannerData.map((data, index) => {
          return (
            <div className="min-w-full min-h-[450px] lg:min-h-full overflow-hidden relative group transition-all" style={{transform: `translateX(${currentImage * -100}%)`}} key={index}>
              <div className="w-full h-full">
                <img
                  src={data.backdropPath}
                  className="w-full h-screen object-cover"
                />
              </div>
              {/*Button next and previous */}
            <div className="absolute top-0 w-full h-full hidden items-center justify-between px-4 group-hover:flex">
                <button className="bg-white p-1 rounded-full text-xl z-10 text-black cursor-pointer" onClick={handlePrevious}>
                  <FaAngleLeft/>
                </button>
                <button className="bg-white p-1 rounded-full text-xl z-10 text-black cursor-pointer" onClick={handleNext}>
                  <FaAngleRight/>
                </button>
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
