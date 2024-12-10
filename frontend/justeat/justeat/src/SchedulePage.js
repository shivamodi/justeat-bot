import { Box, Typography, Slider, Grid, TextField, Paper, Accordion, AccordionSummary, AccordionDetails, Switch, FormControlLabel } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useSidebar } from './SidebarContext'; // Import the custom hook
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Button, Snackbar } from '@mui/material';

// Days of the week (Monday to Sunday)
const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

const SchedulePage = () => {
  
  const username = localStorage.getItem('userName');
  const [message, setMessage] = useState('');

  const { isDrawerOpen, isHamburgerVisible } = useSidebar();
  const [openSnackbar, setOpenSnackbar] = useState(false);

  const [schedule, setSchedule] = useState({
    Monday: { range: [0, 24], enabled: true },
    Tuesday: { range: [0, 24], enabled: true },
    Wednesday: { range: [0, 24], enabled: true },
    Thursday: { range: [0, 24], enabled: true },
    Friday: { range: [0, 24], enabled: true },
    Saturday: { range: [0, 24], enabled: true },
    Sunday: { range: [0, 24], enabled: true },
  });


  // Function to save the schedule data to the backend
  const saveSchedule = async (updatedSchedule) => {
    try {
      // Send the updated schedule data to the server (replace with your actual API endpoint)
      const response = await fetch('https://backend.grabbereat.com/saveschedule', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedSchedule),
      });

      if (response.ok) {
        // Show success message if data is saved successfully
        setMessage('Saved Successfully');
        setOpenSnackbar(true);
        setTimeout(() => {
          setOpenSnackbar(false);
        }, 3000);
      } else {
        console.error('Failed to save schedule data');
        setMessage('Error Saving');
        setOpenSnackbar(true);
        setTimeout(() => {
          setOpenSnackbar(false);
        }, 3000);
      }
    } catch (error) {
      console.error('Error saving schedule data:', error);
      setMessage('Error Saving');
      setOpenSnackbar(true);
      setTimeout(() => {
        setOpenSnackbar(false);
      }, 3000);
    }
  };

  const handleSliderChange = (day, newValue) => {
    // Update the schedule state
    setSchedule((prevSchedule) => {
      const updatedSchedule = {
        ...prevSchedule,
        [day]: {
          ...prevSchedule[day],
          range: newValue,
        },
      };

      // Save the updated schedule to the backend
      saveSchedule(updatedSchedule);

      return updatedSchedule; // Return updated schedule for state
    });
  };

  const handleToggleChange = (day) => {
    // Update the schedule state
    setSchedule((prevSchedule) => {
      const updatedSchedule = {
        ...prevSchedule,
        [day]: {
          ...prevSchedule[day],
          enabled: !prevSchedule[day].enabled,
        },
      };

      // Save the updated schedule to the backend
      saveSchedule(updatedSchedule);

      return updatedSchedule; // Return updated schedule for state
    });
  };

  const handleSubmit = () => {
    // Get CSRF token if needed
    const csrftoken = Cookies.get('csrftoken');
    axios.post('https://backend.grabbereat.com/schedule', {
      username: username
    }, {
      headers: {
        'X-CSRFToken': csrftoken,  // Include CSRF token in the request headers
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      console.log('Login successful:', response.data);
      setMessage('data retrieved successfully')
      //setOpenSnackbar(true);
      setTimeout(() => {
        //setOpenSnackbar(false);
      }, 3000);
      // Handle successful login (e.g., redirect or update UI)
      setSchedule(response.data);
    })
    .catch(error => {
      console.error('Error in schedule:', error);
      // Handle error (e.g., show error message)
      setMessage('Invalid Schedule data')
      //setOpenSnackbar(true);
      setTimeout(() => {
        //setOpenSnackbar(false);
      }, 3000);
    });
  };

  useEffect(() => {
    handleSubmit();
  }, []);
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', padding: '20px', backgroundColor: '#121212', color: 'white', marginLeft: isHamburgerVisible ? '0px' : '250px' }}>
      <Typography variant="h4"  color="white" marginTop="50px" gutterBottom sx={{ color: 'white' }}>Schedule</Typography>

      <Grid container spacing={3}>
        {daysOfWeek.map((day) => (
          <Grid item xs={12} md={6} lg={4} key={day}>
            <Paper sx={{ padding: '10px', backgroundColor: '#1D1D1D' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Typography sx={{ color: 'white', marginBottom: '10px' }}>{day}</Typography>

                <FormControlLabel
                  control={
                    <Switch
                      checked={schedule[day].enabled}
                      onChange={() => handleToggleChange(day)}
                      sx={{
                        '& .MuiSwitch-thumb': {
                          backgroundColor: '#4CAF50', // Green thumb color
                        },
                        '& .MuiSwitch-track': {
                          backgroundColor: '#888', // Light gray track color
                        },
                      }}
                    />
                  }
                  label="Enabled"
                  labelPlacement="end"
                  sx={{ color: 'white' }}
                />
              </Box>

              <Slider
                value={[parseInt(schedule[day].range[0]),parseInt(schedule[day].range[1])]}
                onChange={(event, newValue) => handleSliderChange(day, newValue)}
                valueLabelDisplay="auto"
                valueLabelFormat={(value) => `${value}:00`}
                min={0}
                max={24}
                step={1}
                disabled={!schedule[day].enabled}
                sx={{
                  color: '#4CAF50', // Green accent color for slider
                  '& .MuiSlider-thumb': {
                    backgroundColor: '#4CAF50', // Green thumb color
                  },
                  '& .MuiSlider-rail': {
                    backgroundColor: '#888', // Light gray rail
                  },
                }}
              />

              <Accordion sx={{ backgroundColor: '#333', marginTop: '10px' }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon sx={{ color: 'white' }} />}>
                  <Typography sx={{ color: 'white' }}>View Selected Hours</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography sx={{ color: 'white' }}>
                    Selected time range: {schedule[day].range[0]}:00 - {schedule[day].range[1]}:00
                  </Typography>
                </AccordionDetails>
              </Accordion>
            </Paper>
          </Grid>
        ))}
      </Grid>

            {/* Snackbar message to show the success/failure message */}
      <Snackbar
        open={openSnackbar}
        message={message}
        autoHideDuration={3000}
        onClose={() => setOpenSnackbar(false)}
      />
    </Box>
    
  );
};

export default SchedulePage;
