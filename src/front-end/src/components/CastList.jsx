import React, { useState } from "react";

const CastList = ({ castData }) => {
  const [showAll, setShowAll] = useState(false);

  const filteredCast = castData?.cast?.filter((el) => el?.profile_path) || [];
  const visibleCast = showAll ? filteredCast : filteredCast.slice(0, 14);

  return (
    <div>
      <h2 className="font-bold text-lg text-white">Cast :</h2>
      <div className="grid grid-cols-[repeat(auto-fit,96px)] gap-5 my-4 transition-all">
        {visibleCast.map((starCast, index) => (
          <div key={index} title={starCast.character}>
            <div>
              <img
                alt={starCast.character}
                src={"https://image.tmdb.org/t/p/original" + starCast.profile_path}
                className="w-24 h-24 object-cover rounded-full"
              />
            </div>
            <a href={'/cast/' + starCast.id} className="font-bold text-center text-sm text-neutral-400 underline" >
              {starCast.name}
            </a>
          </div>
        ))}
      </div>

      {filteredCast.length > 14 && (
        <button
          onClick={() => setShowAll(!showAll)}
          className="mt-2 text-sm text-white hover:underline cursor-pointer"
        >
          {showAll ? "Show Less" : "View More"}
        </button>
      )}
    </div>
  );
};

export default CastList;
