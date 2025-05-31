import React, { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import Card from '../components/Card'
const fakeMovieData = [
  {
    "name": "Chronos Echo",
    "director": "Elara Vance",
    "actors": ["Jax Riley", "Seraphina Moon", "Orion Kade"],
    "genres": ["Sci-Fi", "Thriller", "Mystery"],
    "release_date": "2024-03-15",
    "duration": 132, // minutes
    "language": "English",
    "rating": 8.1,
    "description": "A physicist discovers a way to receive echoes from the future, only to uncover a devastating event he must race against time to prevent. But can the future truly be changed?",
    "poster": "https://placehold.co/300x450/E8AA42/000000?text=Chronos+Echo",
    "trailer": "https://www.youtube.com/watch?v=dQw4w9WgXcQ" // Placeholder trailer
  },
  {
    "name": "The Last Verdant Bloom",
    "director": "Marcus Greenwell",
    "actors": ["Willow Aspen", "River Stone", "Clay Forester"],
    "genres": ["Drama", "Post-Apocalyptic", "Adventure"],
    "release_date": "2023-11-08",
    "duration": 118,
    "language": "English",
    "rating": 7.5,
    "description": "In a world choked by pollution, a young botanist embarks on a perilous journey to find the last rumored patch of green, a fabled oasis that might hold the key to humanity's survival.",
    "poster": "https://placehold.co/300x450/2D8148/FFFFFF?text=Verdant+Bloom",
    "trailer": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  },
  {
    "name": "Neon Ghosts of Sector 9",
    "director": "Kaito Tanaka",
    "actors": ["Ren Akira", "Yumi Sato", "Kenjiro Ito"],
    "genres": ["Cyberpunk", "Action", "Crime"],
    "release_date": "2024-07-22",
    "duration": 105,
    "language": "Japanese",
    "rating": 6.9,
    "description": "A renegade detective in a futuristic metropolis hunts a digital phantom responsible for a series of high-tech heists, blurring the lines between reality and the virtual world.",
    "poster": "https://placehold.co/300x450/7F00FF/E0B0FF?text=Neon+Ghosts",
    "trailer": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  },
  {
    "name": "Whispers in the Old Library",
    "director": "Eleanor Ainsworth",
    "actors": ["Arthur Pendelton", "Clara Paige", "Silas Blackwood"],
    "genres": ["Horror", "Supernatural", "Gothic"],
    "release_date": "2023-09-01",
    "duration": 96,
    "language": "English",
    "rating": 7.2,
    "description": "A skeptical historian cataloging an ancient library unleashes a malevolent entity trapped within a forbidden tome. The library's secrets are far darker than he imagined.",
    "poster": "https://placehold.co/300x450/4A4A4A/CCCCCC?text=Old+Library",
    "trailer": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  },
  {
    "name": "The Sunken City of Eldoria",
    "director": "Marina Aqua",
    "actors": ["Coral Reef", "Finn Caspian", "Pearl Oceania"],
    "genres": ["Fantasy", "Adventure", "Family"],
    "release_date": "2024-05-30",
    "duration": 110,
    "language": "English",
    "rating": 7.8,
    "description": "Two young explorers discover a map leading to a legendary underwater city. They must overcome mythical sea creatures and ancient guardians to uncover its lost treasures.",
    "poster": "https://placehold.co/300x450/0077BE/AADDFF?text=Eldoria",
    "trailer": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  },
  {
    "name": " comedic Interstellar Misadventure",
    "director": "Barnaby Chuckles",
    "actors": ["Zany Zoe", "Guffaw Gus", "Silly Sam"],
    "genres": ["Comedy", "Sci-Fi"],
    "release_date": "2023-12-25",
    "duration": 88,
    "language": "English",
    "rating": 6.5,
    "description": "A hapless janitor accidentally launches himself into space on a top-secret starship, leading to a series of bizarre encounters with eccentric aliens and cosmic mishaps.",
    "poster": "https://placehold.co/300x450/FFD700/4B0082?text=Cosmic+Comedy",
    "trailer": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  },
  {
    "name": "Crimson Peak Vigilante",
    "director": "Rex Maverick",
    "actors": ["Blade Ryder", "Scarlett Justice", "Victor Stone"],
    "genres": ["Action", "Western", "Revenge"],
    "release_date": "2024-08-12",
    "duration": 125,
    "language": "English",
    "rating": 7.0,
    "description": "A lone rider, haunted by his past, returns to the lawless town of Crimson Peak to exact revenge on the gang that wronged him, one bullet at a time.",
    "poster": "https://placehold.co/300x450/8B0000/FFEBCD?text=Crimson+Peak",
    "trailer": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  },
  {
    "name": "The Alchemist's Secret Garden",
    "director": "Isabelle Fleur",
    "actors": ["Rosalind Thorne", "Leo Herbalist", "Magnus Aurelius"],
    "genres": ["Mystery", "Historical Fiction", "Drama"],
    "release_date": "2023-10-19",
    "duration": 140,
    "language": "French",
    "rating": 8.3,
    "description": "In 17th century Paris, a young apprentice uncovers her master alchemist's hidden garden, a place of wondrous plants and dangerous secrets that could change the world or destroy it.",
    "poster": "https://placehold.co/300x450/556B2F/FFFACD?text=Alchemist+Garden",
    "trailer": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  },
  {
    "name": "Zero Gravity Heist",
    "director": "Ace Sterling",
    "actors": ["Nova Starr", "Bolt Jackson", "Quasar Ray"],
    "genres": ["Action", "Sci-Fi", "Heist"],
    "release_date": "2024-01-05",
    "duration": 100,
    "language": "English",
    "rating": 6.7,
    "description": "A team of elite thieves plans an audacious robbery on a heavily fortified space station. Their biggest challenge? Performing the heist in zero gravity while evading a relentless security chief.",
    "poster": "https://placehold.co/300x450/C0C0C0/1A1A1A?text=Zero+G+Heist",
    "trailer": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  },
  {
    "name": "Melody of the Lost Kingdom",
    "director": "Seren Lyra",
    "actors": ["Aria Song", "Cadence Rhapsody", "Orpheus Strings"],
    "genres": ["Musical", "Fantasy", "Romance"],
    "release_date": "2024-06-10",
    "duration": 128,
    "language": "English",
    "rating": 7.9,
    "description": "A wandering minstrel with a magical lute stumbles upon a hidden kingdom where music has been forbidden. Her songs begin to reawaken its forgotten magic and a forbidden love.",
    "poster": "https://placehold.co/300x450/DA70D6/FFFFFF?text=Lost+Melody",
    "trailer": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  }
];

const TheaterMovies = () => {
  return (
    <div className='py-16'>
        <div className='container mx-auto'>
          <h3 className='capitalize text-lg lg:text-xl font-semibold my-3'>Search Results</h3>
          <div className='grid grid-cols-[repeat(auto-fit,260px)] gap-6 justify-center lg:justify-start'>
              {
                fakeMovieData.map((movie,index)=>{
                  return(
                    <Card data={movie} key={index+"search"} trending={false} />
                  )
                })
              }
          </div>

        </div>
    </div>
  )
}

export default TheaterMovies