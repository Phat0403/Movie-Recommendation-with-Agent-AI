import React from "react";
import BannerHome from "../components/BannerHome";
import { useQuery } from "@tanstack/react-query";
import { FaAngleRight } from "react-icons/fa6";
import { FaAngleLeft } from "react-icons/fa6";
import { useEffect, useState } from "react";
import Card from "../components/Card";
import HorizontalScrollCard from "../components/HorizontalScrollCard";

const Home = () => {
  const {
    data: bannerData = [],
    isLoading,
    error,
  } = useQuery({
    queryKey: ["movies"],
    queryFn: () =>
      fetch("http://localhost:8000/api/movies/ratings").then((res) => {
        if (!res.ok) {
          throw new Error("Network response was not ok");
        }
        return res.json();
      }),
  });

  return (
    <div>
      <BannerHome bannerData={bannerData} />
      <HorizontalScrollCard data={bannerData} heading={"Trending"}/>
    </div>
  );
};

export default Home;
