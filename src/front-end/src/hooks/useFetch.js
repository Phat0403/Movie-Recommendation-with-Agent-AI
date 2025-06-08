// useFetch.js
import { useQuery } from '@tanstack/react-query';

export const useFetch = (endpoint, key) => {
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
      return res.json();
    },
  });

  return { data, isLoading, error };
};

