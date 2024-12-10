import React from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const CancelPage = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="sm" sx={{ marginTop: '50px' }}>
      <Box sx={{ textAlign: 'center', padding: '20px' }}>
        <Typography  color="white" marginTop="50px" variant="h4" gutterBottom>
          Payment Canceled
        </Typography>
        <Typography variant="body1" color="textSecondary" paragraph>
          You have canceled the payment. If you need help, feel free to contact us.
        </Typography>
        <Button
          variant="contained"
          color="secondary"
          onClick={() => navigate('/dash')}  // Redirecting to the home page or a relevant page
        >
          Return to Home
        </Button>
      </Box>
    </Container>
  );
};

export default CancelPage;
