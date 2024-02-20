// ExportButton.js
import React from 'react';
import axios from 'axios';
import { Button } from '@mui/material';
import { lightGreen } from '@mui/material/colors';
import * as XLSX from 'xlsx';
import DownloadIcon from '@mui/icons-material/Download';

const ExportButton = ({ selectedId }) => {
  const fetchDetailsAndExport = async () => {
    // making sure selected ID is correct
    console.log('Selected ID:', selectedId);
    try {
      const response = await axios.get(`http://localhost:8000/data/get-details?id=${selectedId}`);
      const details = response.data;
      const ws = XLSX.utils.json_to_sheet(details);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "PaymentData");
      XLSX.writeFile(wb, "PaymentData.xlsx");
    } catch (error) {
      console.error('Error fetching details:', error);
    }
  };

  return (
    <Button 
        onClick={fetchDetailsAndExport} 
        variant="contained" 
        sx={{ bgcolor: lightGreen[500], '&:hover': { bgcolor: lightGreen[700] } }}
        startIcon={<DownloadIcon />} 
        disabled={!selectedId}
    >
      Export
    </Button>
  );
};

export default ExportButton;
