import React from "react";
import { useLocation } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { useFetchTheMovieDb } from "../hooks/useFetchCast";
import { useFetch } from "../hooks/useFetch"; 
import HorizontalScrollCard from "../components/HorizontalScrollCard";
const TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/";

const DetailItem = ({ label, value, isLink, href }) => {
  // ... (Không thay đổi)
  if (!value && value !== 0) return null;
  return (
    <div className="mb-2 flex">
      <strong className="w-36 text-neutral-300 font-medium shrink-0">
        {label}:
      </strong>
      {isLink && href ? (
        <a
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sky-400 hover:text-sky-300 hover:underline transition-colors break-words"
        >
          {value}
        </a>
      ) : (
        <span className="text-neutral-100 break-words">{value}</span>
      )}
    </div>
  );
};

const CastDetailPage = () => {
  const location = useLocation();
  const castId = location.pathname.split("/").pop();
  
  const {
    data: castMember,
    isLoading: isLoadingCastMember, // Đổi tên để tránh trùng lặp
    isError: isErrorCastMember,     // Đổi tên để tránh trùng lặp
  } = useFetchTheMovieDb(`/person/${castId}?language=en-US`);

  const {
    data: movieByCast, 
    isLoading: isLoadingMovies,
    error: errorMovies,
  } = useQuery({
  
    queryKey: ['moviesByCast', castMember?.imdb_id],
    queryFn: async () => {
      const res = await fetch(`http://localhost:8000/api/movies/by/${castMember.imdb_id}`);
      if (!res.ok) {
        throw new Error("Network response was not ok");
      }
      return res.json();
    },
    enabled: !!castMember?.imdb_id, 
  });

  if (isLoadingCastMember) {
    return <div>Loading cast member details...</div>;
  }

  if (isErrorCastMember) {
    return <div>Error loading cast member details.</div>;
  }

  const profileImageUrl = castMember?.profile_path
    ? `${TMDB_IMAGE_BASE_URL}w500${castMember.profile_path}`
    : `https://via.placeholder.com/500x750.png?text=${encodeURIComponent(
        castMember?.name?.split(" ").join("+") || "No+Image"
      )}`;

  console.log("Cast Member Data:", castMember); 
  console.log("Movie by Cast Data:", movieByCast); 

  const getGenderString = (gender) => {
    switch (gender) {
      case 1: return "Female";
      case 2: return "Male";
      case 3: return "Non-binary";
      default: return "Not specified";
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return null;
    return new Date(dateString).toLocaleDateString(undefined, {
      year: "numeric", month: "long", day: "numeric",
    });
  };

  return (
    <div className="container mx-auto p-4 md:p-8 mt-10">
      <div className="flex flex-col md:flex-row gap-8 mb-10">
        <div className="w-full md:w-auto md:flex-shrink-0">
          <img
            src={profileImageUrl}
            alt={castMember?.name}
            className="w-60 h-90 md:w-72 md:h-[432px] object-cover rounded-lg shadow-2xl mx-auto md:mx-0 border-2 border-neutral-700"
          />
        </div>
        <div className="flex-grow text-center md:text-left">
          <h1 className="text-4xl lg:text-5xl font-bold text-white mb-3">
            {castMember?.name}
          </h1>

          <div className="mb-6">
            <h2 className="text-xl font-semibold text-neutral-200 mb-2 border-b border-neutral-700 pb-1">
              Personal Information
            </h2>
            <DetailItem
              label="Known For"
              value={castMember?.known_for_department}
            />
            <DetailItem
              label="Gender"
              value={getGenderString(castMember?.gender)}
            />
            <DetailItem
              label="Birthday"
              value={formatDate(castMember?.birthday)}
            />
            {castMember?.deathday && (
              <DetailItem
                label="Day of Death"
                value={formatDate(castMember?.deathday)}
              />
            )}
            <DetailItem
              label="Place of Birth"
              value={castMember?.place_of_birth}
            />
            <DetailItem
              label="Popularity"
              value={castMember?.popularity?.toFixed(2)}
            />
            {castMember?.imdb_id && (
              <DetailItem
                label="IMDb"
                value={`View on IMDb (ID: ${castMember?.imdb_id})`}
                isLink={true}
                href={`https://www.imdb.com/name/${castMember?.imdb_id}`}
              />
            )}
            {castMember?.homepage && (
              <DetailItem
                label="Homepage"
                value={castMember?.homepage}
                isLink={true}
                href={castMember?.homepage}
              />
            )}
          </div>

          {castMember?.biography && (
            <div className="mb-6">
              <h2 className="text-xl font-semibold text-neutral-200 mb-2 border-b border-neutral-700 pb-1">
                Biography
              </h2>
              <p className="text-neutral-300 whitespace-pre-line leading-relaxed text-sm">
                {castMember?.biography}
              </p>
            </div>
          )}

          {castMember?.also_known_as &&
            castMember?.also_known_as.length > 0 && (
              <div className="mb-6">
                <h2 className="text-xl font-semibold text-neutral-200 mb-2 border-b border-neutral-700 pb-1">
                  Also Known As
                </h2>
                <ul className="list-disc list-inside text-neutral-300 text-sm">
                  {castMember?.also_known_as.map((name, index) => (
                    <li key={index}>{name}</li>
                  ))}
                </ul>
              </div>
            )}
        </div>
      </div>
            <HorizontalScrollCard data={movieByCast} heading="Movies by Cast" />
      {isLoadingMovies && <div>Loading movies...</div>}
      {errorMovies && <div>Error loading movies.</div>}
    </div>
  );
};

export default CastDetailPage;