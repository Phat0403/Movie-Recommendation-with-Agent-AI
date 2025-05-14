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
      <div className="flex min-h-full max-h-[95hv]">
        {bannerData.map((data, index) => {
          return (
            <div className="min-w-full min-h-[450px] lg:min-h-full overflow-hidden">
              <div className="w-full h-full">
                <img src={data.backdropPath} 
                className="w-full h-screen object-cover"
                />
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default BannerHome;
