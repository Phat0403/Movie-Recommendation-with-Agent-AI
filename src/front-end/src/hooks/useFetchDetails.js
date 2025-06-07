// useFetch.js
import { useQuery } from '@tanstack/react-query';

export const useFetchDetails = (endpoint, key) => {
  const {
    data = [],
    isLoading,
    error,
  } = useQuery({
    queryKey: [endpoint],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api'+endpoint);
      if (!res.ok) {
        throw new Error("Network response was not ok");
      }
      const result = await res.json();
      return Array.isArray(result) ? result[0] : result;
    },
  });

  return { data, isLoading, error };
};

