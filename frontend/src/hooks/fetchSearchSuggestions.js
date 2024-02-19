import { useState, useEffect } from 'react';
import axios from 'axios';
import debounce from 'lodash.debounce';

export default function useSearchSuggestions(query) {
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    const fetchSuggestions = debounce(async () => {
      if (query.length < 3) return;  // Only search if the query is at least 3 characters
      try {
        const response = await axios.get(`http://backend:8000/search`, { params: { query } });
        setSuggestions(response.data || []);
      } catch (error) {
        console.error("Error fetching search suggestions:", error);
      }
    }, 300);

    fetchSuggestions();
    return () => fetchSuggestions.cancel();
  }, [query]);

  return suggestions;
}
