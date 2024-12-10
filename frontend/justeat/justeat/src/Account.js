import React, { useState, useEffect } from 'react';
import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Button,
  TextField,
  Typography,
  Box,
  Snackbar,
  Switch,
  FormControlLabel,
  InputAdornment,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom'; // Import Link for routing
import { useSidebar } from './SidebarContext'; // Import the custom hook
import Cookies from 'js-cookie';

// Dark theme configuration
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#1976d2', // Adjust this for your color scheme
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
    text: {
      primary: '#fff',
      secondary: '#b0bec5',
    },
  },
  typography: {
    fontFamily: 'Poppins, sans-serif',
  },
});

function Account() {
  const username = localStorage.getItem('userName');  
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [notifications, setNotifications] = useState({
    emailNotifications: true,
    whatsappNotifications: true,
    email: '',
    whatsapp: '',
  });
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const { isDrawerOpen, isHamburgerVisible } = useSidebar();

  const handleNotificationsUpdate = async () => {
    try {
      const response = await axios.post('https://backend.grabbereat.com/savenotifications', { settings: notifications });
      setSnackbarMessage('Notifications updated successfully');
      setOpenSnackbar(true);
    } catch (error) {
      setSnackbarMessage('Error updating notifications.');
      setOpenSnackbar(true);
    }
  };

  const handlePasswordChange = async () => {
    if (newPassword !== confirmPassword) {
      setSnackbarMessage('Passwords do not match.');
      setOpenSnackbar(true);
      return;
    }
    try {
      const response = await axios.post('https://backend.grabbereat.com/saveprofile', {
        username,
        currentPassword,
        newPassword,
      });
      setSnackbarMessage('Password changed successfully!');
      setOpenSnackbar(true);
    } catch (error) {
      setSnackbarMessage('Error changing password.');
      setOpenSnackbar(true);
    }
  };

  const handleSubmit = () => {
    // Get CSRF token if needed
    const csrftoken = Cookies.get('csrftoken');
    axios.post('https://backend.grabbereat.com/notifications', {
      username: username
    }, {
      headers: {
        'X-CSRFToken': csrftoken,  // Include CSRF token in the request headers
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      console.log('Notifications retrieved successfully:', response.data);
      //setSnackbarMessage('Data retrieved successfully');
      //setOpenSnackbar(true);
      setNotifications(response.data);
      return;
    })
    .catch(error => {
      console.error('Error in notification retrieval:', error);
      //setSnackbarMessage('Invalid schedule data');
      //setOpenSnackbar(true);
      return;
    });
  };

  useEffect(() => {
    handleSubmit();
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ marginLeft: 'auto', marginRight: 'auto', padding: '20px', marginLeft: isHamburgerVisible ? '0px' : '250px' }}>
        
      <Box sx={{ padding: '20px', alignContent: 'center'}}>
        <Typography color="white" marginTop="50px" variant="h4" align="center" gutterBottom>
          Account Settings
        </Typography>


        {/* Notifications Section */}
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="notifications-content" id="notifications-header">
            <Typography>Notifications</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Box>
              <Typography variant="body1" color="text.primary" paragraph>
                Manage your notification preferences.
              </Typography>

              {/* Email Notifications */}
              <TextField
                label="Email Address for Notifications"
                fullWidth
                value={notifications.email}
                onChange={(e) => setNotifications({ ...notifications, email: e.target.value })}
                variant="outlined"
                color="primary"
                sx={{ marginBottom: '20px' }}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <FormControlLabel
                        control={
                          <Switch
                            checked={notifications.emailNotifications}
                            onChange={(e) =>
                              setNotifications({
                                ...notifications,
                                emailNotifications: e.target.checked,
                              })
                            }
                            name="emailNotifications"
                          />
                        }
                      />
                    </InputAdornment>
                  ),
                }}
              />

              {/* WhatsApp Notifications */}
              <TextField
                label="WhatsApp Number for Notifications"
                fullWidth
                value={notifications.whatsapp}
                onChange={(e) => setNotifications({ ...notifications, whatsapp: e.target.value })}
                variant="outlined"
                color="primary"
                sx={{ marginBottom: '20px' }}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <FormControlLabel
                        control={
                          <Switch
                            checked={notifications.whatsappNotifications}
                            onChange={(e) =>
                              setNotifications({
                                ...notifications,
                                whatsappNotifications: e.target.checked,
                              })
                            }
                            name="whatsappNotifications"
                          />
                        }
                      />
                    </InputAdornment>
                  ),
                }}
              />

              <Button variant="contained" color="primary" onClick={handleNotificationsUpdate}>
                Update Notifications
              </Button>
            </Box>
          </AccordionDetails>
        </Accordion>

        {/* Change Password Section */}
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls="password-content" id="password-header">
            <Typography>Change Password</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Box>
              <Typography variant="body1" color="text.primary" paragraph>
                Change your current password.
              </Typography>
              <TextField
                label="Current Password"
                type="password"
                fullWidth
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                variant="outlined"
                color="primary"
                sx={{ marginBottom: '20px' }}
              />
              <TextField
                label="New Password"
                type="password"
                fullWidth
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                variant="outlined"
                color="primary"
                sx={{ marginBottom: '20px' }}
              />
              <TextField
                label="Confirm New Password"
                type="password"
                fullWidth
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                variant="outlined"
                color="primary"
                sx={{ marginBottom: '20px' }}
              />
              <Button variant="contained" color="primary" onClick={handlePasswordChange}>
                Change Password
              </Button>
            </Box>
          </AccordionDetails>
        </Accordion>

        {/* Snackbar for showing messages */}
        <Snackbar
          open={openSnackbar}
          autoHideDuration={3000}
          message={snackbarMessage}
          onClose={() => setOpenSnackbar(false)}
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        />
      </Box>
      </Box>
    </ThemeProvider>
  );
}

export default Account;
