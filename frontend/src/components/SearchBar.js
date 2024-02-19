import React, { useState } from 'react';
import axios from 'axios';
import { Typography, Box, TextField } from '@mui/material';

const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);

  const fetchSearchSuggestions = async (query) => {
    try {
      console.log('Fetching suggestions for query:', query);
      const response = await axios.get(`http://localhost:9200/general_payments_index/_search?q=${query}`);
      console.log('Response:', response.data);
      setSuggestions(response.data); // Assume the response directly provides suggestions
    } catch (error) {
      console.error('Error fetching suggestions:', error);
    }
  };

  const handleInputChange = (event) => {
    const newValue = event.target.value;
    console.log('Input changed:', newValue);
    setQuery(newValue);
    fetchSearchSuggestions(newValue);
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        marginTop: '10vh'
      }}
    >
      <Typography variant='h4' component='h1'>React Search Bar</Typography>
      <TextField
        label="Search title"
        value={query}
        onChange={handleInputChange}
        sx={{ width: '50%' }}
      />
      {/* Display suggestions */}
      <ul>
        {suggestions.map((suggestion, index) => (
          <li key={index}>{suggestion.name}</li>
        ))}
      </ul>
    </Box>
  );
};

export default SearchBar;
