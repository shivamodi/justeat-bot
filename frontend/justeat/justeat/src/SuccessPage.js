import React, { useEffect } from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const SuccessPage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // You can add any logic here, such as tracking the session or displaying additional messages
    // For example, sending success data to your backend, etc.
  }, []);

  return (
    <Container maxWidth="sm" sx={{ marginTop: '50px' }}>
      <Box sx={{ textAlign: 'center', padding: '20px' }}>
        <Typography color="white" variant="h4" gutterBottom>
          Payment Successful!
        </Typography>
        <Typography variant="body1" color="white" paragraph>
          Your payment was successfully processed. Thank you for your purchase!
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate('/dash')}  // Redirecting to the home page or any page you want after success
        >
          Go to Dashboard
        </Button>
      </Box>
    </Container>
  );
};

export default SuccessPage;
