import React, { useState } from 'react';
import axios from 'axios';
import { Typography, Box, TextField, List, ListItem, Paper,Grid } from '@mui/material';

const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);

  const fetchSearchSuggestions = async (query) => {
    try {
      console.log('Fetching suggestions for query:', query);
      const response = await axios.get(`http://localhost:8000/search?query=${query}`);
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
    if (newValue) {
      fetchSearchSuggestions(newValue);
    } else {
      setSuggestions([]); // clear suggestions if input is cleared
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        marginTop: '10vh',
        width: '100%',
      }}
    >
      <Typography variant='h4' component='h1'>Payments</Typography>
      <TextField
        label="Search title"
        value={query}
        onChange={handleInputChange}
        sx={{ width: '50%', mb: 2 }}
      />
      {/* Display suggestions in a Paper component for elevation */}
      <Paper sx={{ width: '50%', maxHeight: 300, overflow: 'auto', mt: 2 }}>
        <List>
          {suggestions.map((suggestion, index) => (
            <ListItem key={index}>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Typography variant="subtitle1">{suggestion.first_name} {suggestion.middle_name} {suggestion.last_name}</Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="body2" color="textSecondary">Amount: ${suggestion.hospital_name}</Typography>
                </Grid>
              </Grid>
            </ListItem>
          ))}
        </List>
      </Paper>
    </Box>
  );
};

export default SearchBar;
