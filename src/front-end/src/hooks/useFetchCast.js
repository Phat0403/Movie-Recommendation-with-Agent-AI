import { useQuery } from '@tanstack/react-query';

export const useFetchTheMovieDb = (endpoint, key) => {
  console.log('https://api.themoviedb.org/3'+endpoint)
  const {
    data = [],
    isLoading,
    error,
  } = useQuery({
    queryKey: [endpoint,key],
    queryFn: async () => {
      const res = await fetch('https://api.themoviedb.org/3'+endpoint, {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2Nzg5Y2JkOWNlM2MyZjk1MzI0ZGM5N2FhMmU0YWUyZCIsIm5iZiI6MTc0NDYwMjA3NC40NTEsInN1YiI6IjY3ZmM4M2RhZGU1ZTRkZWM2MmFlMjBkOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.m6K4NYFCWDM631dwC8P8UvCYRab8fXDBIlNH4jnS9VQ',
        'accept': 'application/json'
        },
      }
        
      );
      if (!res.ok) {
        throw new Error("Network response was not ok");
      }
      const result = await res.json();
      return result;
    },
  });

  return { data, isLoading, error };
};
