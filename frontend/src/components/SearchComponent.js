import React, { useState } from 'react';
import fetchSearchSuggestions from '../hooks/fetchSearchSuggestions'
import { Typography, Box, TextField, Autocomplete } from '@mui/material'

const SearchComponent = () => {
  const [query, setQuery] = useState('');
  const suggestions = fetchSearchSuggestions(query);

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
      <Autocomplete
        disablePortal
        id='combo-box-demo'
        sx={{
          width: '50%',
          margin: '20px auto',
        }}
        renderInput={(params) => <TextField {...params} label='Search title' />}
      />
      {/* Render suggestions */}
    </Box>
  );
};

export default SearchComponent;
