// import React, { useState, useEffect } from 'react';
// import { UserCircleIcon, HeartIcon, ChatBubbleLeftRightIcon, ArrowLeftIcon, FilmIcon } from './icons';


// const ProfilePage= ({ allMovies, onNavigateBack }) => {
//   const [userData, setUserData] = useState(null);
//   const [isLoading, setIsLoading] = useState(true);
//   const [error, setError] = useState<string | null>(null);

//   useEffect(() => {
//     const loadUserData = async () => {
//       setIsLoading(true);
//       setError(null);
//       try {
//         const data = await fetchUserInfo();
//         setUserData(data);
//       } catch (err) {
//         setError(err.message || 'Failed to fetch user profile.');
//         console.error("ProfilePage fetch error:", err);
//       } finally {
//         setIsLoading(false);
//       }
//     };
//     loadUserData();
//   }, []);

//   const getMovieTitleById = (movieId)=> {
//     const movie = allMovies.find(m => m.id === movieId);
//     return movie ? movie.title : `ID: ${movieId}`;
//   };
  
//   const getMoviePosterById = (movieId) => {
//     const movie = allMovies.find(m => m.id === movieId);
//     // Use picsum for a placeholder if actual posterPath isn't directly usable or needs base URL
//     return movie ? `https://picsum.photos/seed/${movie.id}/100/150` : `https://picsum.photos/seed/${movieId}/100/150`;
//   };


//   if (isLoading) {
//     return (
//       <div className="flex justify-center items-center h-64">
//         <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-sky-500"></div>
//         <p className="ml-4 text-lg text-gray-300">Loading Profile...</p>
//       </div>
//     );
//   }

//   if (error) {
//     return (
//       <div className="text-center p-8 bg-neutral-700 rounded-lg shadow-xl">
//         <h2 className="text-2xl font-semibold text-red-400 mb-4">Error Loading Profile</h2>
//         <p className="text-gray-300 mb-6">{error}</p>
//         <button
//           onClick={onNavigateBack}
//           className="bg-sky-600 hover:bg-sky-700 text-white font-semibold py-2 px-6 rounded-md transition-colors flex items-center mx-auto"
//         >
//           <ArrowLeftIcon className="w-5 h-5 mr-2" />
//           Back to Home
//         </button>
//       </div>
//     );
//   }

//   if (!userData) {
//     return (
//       <div className="text-center p-8">
//         <p className="text-lg text-gray-400">No user data found.</p>
//          <button
//           onClick={onNavigateBack}
//           className="mt-6 bg-sky-600 hover:bg-sky-700 text-white font-semibold py-2 px-6 rounded-md transition-colors flex items-center mx-auto"
//         >
//           <ArrowLeftIcon className="w-5 h-5 mr-2" />
//           Back to Home
//         </button>
//       </div>
//     );
//   }

//   return (
//     <div className="max-w-4xl mx-auto p-4 md:p-6 bg-neutral-800 text-gray-200 rounded-lg">
//       <button
//         onClick={onNavigateBack}
//         className="mb-6 inline-flex items-center text-sky-400 hover:text-sky-300 transition-colors group"
//       >
//         <ArrowLeftIcon className="w-5 h-5 mr-2 transform group-hover:-translate-x-1 transition-transform" />
//         Back to Home
//       </button>

//       {/* User Info Section */}
//       <section className="mb-8 p-6 bg-neutral-700 rounded-xl shadow-xl flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-6">
//         <UserCircleIcon className="w-24 h-24 text-sky-500 flex-shrink-0" />
//         <div className="text-center sm:text-left">
//           <h1 className="text-3xl font-bold text-white">{userData.username}</h1>
//           <p className="text-md text-gray-400">Email: {userData.username}@example.com <span className="text-xs">(placeholder)</span></p>
//         </div>
//       </section>

//       {/* Favorite Movies Section */}
//       <section className="mb-8">
//         <h2 className="text-2xl font-semibold text-white mb-4 flex items-center">
//           <HeartIcon className="w-7 h-7 mr-3 text-red-500" />
//           Favorite Movies
//         </h2>
//         {userData.favorite_movies && userData.favorite_movies.length > 0 ? (
//           <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
//             {userData.favorite_movies.map((movieId) => (
//               <div key={movieId} className="bg-neutral-700 p-4 rounded-lg shadow-lg hover:shadow-sky-500/30 transition-shadow">
//                 <img 
//                   src={getMoviePosterById(movieId)} 
//                   alt={getMovieTitleById(movieId)} 
//                   className="w-full h-48 object-cover rounded-md mb-2 bg-neutral-600" 
//                 />
//                 <h3 className="text-md font-medium text-gray-100 truncate" title={getMovieTitleById(movieId)}>
//                   {getMovieTitleById(movieId)}
//                 </h3>
//                  {getMovieTitleById(movieId).startsWith("ID:") && <p className="text-xs text-gray-500">(Title not found in local data)</p>}
//               </div>
//             ))}
//           </div>
//         ) : (
//           <p className="text-gray-400 italic">No favorite movies listed.</p>
//         )}
//       </section>

//       {/* Comments Section */}
//       <section>
//         <h2 className="text-2xl font-semibold text-white mb-4 flex items-center">
//           <ChatBubbleLeftRightIcon className="w-7 h-7 mr-3 text-green-500" />
//           My Comments
//         </h2>
//         {userData.comments && userData.comments.length > 0 ? (
//           <ul className="space-y-4">
//             {userData.comments.map((commentObj, index) => {
//               const movieId = Object.keys(commentObj)[0];
//               const commentText = commentObj[movieId];
//               return (
//                 <li key={index} className="bg-neutral-700 p-4 rounded-lg shadow-lg">
//                   <p className="text-sm text-gray-300 mb-1">
//                     <span className="font-semibold text-sky-400">{getMovieTitleById(movieId)}:</span> "{commentText.trim()}"
//                   </p>
//                   {getMovieTitleById(movieId).startsWith("ID:") && <p className="text-xs text-gray-500">(Title for comment not found in local data)</p>}
//                 </li>
//               );
//             })}
//           </ul>
//         ) : (
//           <p className="text-gray-400 italic">No comments made yet.</p>
//         )}
//       </section>
//     </div>
//   );
// };

// export default ProfilePage;
