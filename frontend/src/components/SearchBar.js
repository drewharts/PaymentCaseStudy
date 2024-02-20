import React, { useState } from 'react';
import axios from 'axios';
import { Typography, Box, TextField, List, ListItem, Paper,Grid, Stack } from '@mui/material';
import ExportButton from './ExportButton';
import DOMPurify from 'dompurify';

const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [selectedId, setSelectedId] = useState('');

  const fetchSearchSuggestions = async (query) => {
    try {
      console.log('Fetching suggestions for query:', query);
      const response = await axios.get(`http://localhost:8000/search/elasticsearch?query=${query}`);
      console.log('Response:', response.data);
      setSuggestions(response.data);
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
        width: '100%',
      }}
    >
      <Typography variant='h4' component='h1' sx={{ mb: 4 }}>Payments</Typography>
      
      <Stack direction="row" spacing={2} alignItems="center" sx={{ width: '50%', mb: 2 }}>
        <TextField
          label="Search payment"
          value={query}
          onChange={handleInputChange}
          fullWidth 
        />
        {selectedId && <ExportButton selectedId={selectedId} />}

      </Stack>

      {suggestions.length > 0 && (
        <Paper sx={{ width: '50%', maxHeight: 300, overflow: 'auto', mt: 2 }}>
          <List>
            {suggestions.map((suggestion, index) => (
              <ListItem key={index} button onClick={() => setSelectedId(suggestion.id)}>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <Typography variant="subtitle1">{suggestion.first_name} {suggestion.middle_name} {suggestion.last_name}</Typography>
                  </Grid>
                  <Grid item xs={12}>
                  {/* Check if highlight exists and has at least one field */}
                  {suggestion.highlight && Object.keys(suggestion.highlight).length > 0 && (
                    <div 
                      dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(suggestion.highlight[Object.keys(suggestion.highlight)[0]]) }}
                      style={{ textShadow: '0 0 5px yellow' }}
                    />
                  )}
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="body2" color="textSecondary">Amount: ${suggestion.amount}</Typography>
                  </Grid>
                </Grid>
              </ListItem>
            ))}
          </List>
        </Paper>
      )}
    </Box>
  );
};

export default SearchBar;