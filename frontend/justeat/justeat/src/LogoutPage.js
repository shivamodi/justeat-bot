import React, { useEffect } from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const LogoutPage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Clear the 'isAuthenticated' flag from localStorage
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('userName');
    localStorage.removeItem('email');
    localStorage.removeItem('justEatCredentials');
    localStorage.removeItem('currentPlan');
    localStorage.removeItem('firstname');
    localStorage.removeItem('lastname');
    localStorage.removeItem('open_runs_toggle');
    localStorage.removeItem('overflows_toggle');

    // Optionally, you can also clear any other user-related data here (like user info)

    // Redirect the user to the login page (or home page)
    navigate('/signIn');  // Redirecting to a login page or home page after logout
  }, [navigate]);

  return (
    <Container maxWidth="sm" sx={{ marginTop: '50px', textAlign: 'center' }}>
      <Box sx={{ padding: '20px' }}>
        <Typography variant="h4" gutterBottom>
          Logging Out...
        </Typography>
        <Typography variant="body1" color="textSecondary" paragraph>
          You are being logged out. Please wait...
        </Typography>
        {/* Optionally, you can add a spinner or loading indicator here */}
      </Box>
    </Container>
  );
};

export default LogoutPage;
