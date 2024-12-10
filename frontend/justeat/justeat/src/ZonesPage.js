import React, { useState, useEffect } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import {
  Container, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Button,
  Dialog, DialogActions, DialogContent, DialogTitle, TextField, Typography, Box, Paper,
  IconButton, Switch
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { useSidebar } from './SidebarContext'; // Import the custom hook
import axios from 'axios';
import Cookies from 'js-cookie';
import { Snackbar } from '@mui/material';

// Dark theme configuration
const theme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const ZonesPage = () => {
  const [zones, setZones] = useState([
  ]);
  const [searchQuery, setSearchQuery] = useState('');

  
  const username = localStorage.getItem('userName');
  const [message, setMessage] = useState('');

  const { collapsed } = useSidebar();
  const [openSnackbar, setOpenSnackbar] = useState(false);

  const handleSubmit = () => {
    // Get CSRF token if needed
    const csrftoken = Cookies.get('csrftoken');
    axios.post('https://backend.grabbereat.com/zones', {
      username: username
    }, {
      headers: {
        'X-CSRFToken': csrftoken,  // Include CSRF token in the request headers
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      console.log('successful:', response.data);
      
      if (response.data.zones && response.data.zones.length > 0) {
        setMessage('Data retrieved successfully');
        //setOpenSnackbar(true);
        setZones(response.data.zones); // Populate zones only if data exists
      } else {
        setMessage('No zones available');
        //setOpenSnackbar(true);
        setZones([]); // Set zones to an empty array if no zones are available
      }
      
      setTimeout(() => {
        //setOpenSnackbar(false);
      }, 3000);
    })
    .catch(error => {
      console.error('Error in schedule:', error);
      // Handle error (e.g., show error message)
      setMessage('Invalid Schedule data');
      //setOpenSnackbar(true);
      setTimeout(() => {
        //setOpenSnackbar(false);
      }, 3000);
    });
  };

  useEffect(() => {
    handleSubmit();
  }, []);

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value.toLowerCase());
  };

  const handleToggleZone = (zoneName) => {
    // Update the state with the new 'active' value for the toggled zone
    const updatedZones = zones.map(zone =>
      zone.name === zoneName ? { ...zone, active: !zone.active } : zone
    );
  
    // Find the updated zone
    const updatedZone = updatedZones.find(zone => zone.name === zoneName);
  
    // Send the updated zone to the backend
    const csrftoken = Cookies.get('csrftoken');
    axios.post('https://backend.grabbereat.com/save_zone', {
      username, 
      zones: [updatedZone] // Send only the updated zone
    }, {
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      console.log('successful:', response.data);
      setMessage('zones data saved successfully');
      setOpenSnackbar(true);
      setTimeout(() => {
        setOpenSnackbar(false);
      }, 3000);
      // Update the state with the new zone data from the response
      setZones(response.data.zones);
    })
    .catch(error => {
      console.error('Error in schedule:', error);
      setMessage('zones data not saved');
      setOpenSnackbar(true);
      setTimeout(() => {
        setOpenSnackbar(false);
      }, 3000);
    });
  };
  

  const filteredZones = zones.filter(zone => zone.name.toLowerCase().includes(searchQuery) || zone.description.toLowerCase().includes(searchQuery));

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="lg" sx={{ paddingTop: 4 }}>
        <Typography color="white" marginTop="50px" variant="h4" gutterBottom>
          Manage Zones
        </Typography>

        
        <TableContainer component={Paper}>
          <Table aria-label="zones table">
            <TableHead>
              <TableRow>
                <TableCell>Zone Name</TableCell>
                <TableCell>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredZones.map((zone) => (
                <TableRow key={zone.id}>
                  <TableCell>{zone.name}</TableCell>
                  <TableCell>
                    <Switch
                      checked={zone.active}
                      onChange={() => handleToggleZone(zone.name)}
                      name="zoneStatus"
                      color="primary"
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <Snackbar
        open={openSnackbar}
        message={message}
        autoHideDuration={3000}
        onClose={() => setOpenSnackbar(false)}
      />
      </Container>
    </ThemeProvider>
  );
};

export default ZonesPage;
