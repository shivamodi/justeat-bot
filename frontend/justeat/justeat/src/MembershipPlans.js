import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Grid, Card, CardContent, Button, Snackbar, List, ListItem, ListItemText, Divider } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import axios from 'axios';

const theme = createTheme({
  palette: {
    mode: 'dark',
  },
});


const MembershipPlans = () => {
  const username = localStorage.getItem('userName'); // Assuming username is saved in local storage
  const [plans, setPlans] = useState([]);
  const [message, setMessage] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);

  // Fetch plans data from the backend API
  useEffect(() => {
    axios.get('https://backend.grabbereat.com/get_plans')
      .then((response) => {
        setPlans(response.data.plans);  // Assuming the response contains the 'plans' array
        setMessage('Plans data loaded successfully');
        //setOpenSnackbar(true);
      })
      .catch((error) => {
        console.error('Error fetching plans:', error);
        setMessage('Failed to load plans data');
        //setOpenSnackbar(true);
      });
  }, []);

  // Close the snackbar
  const handleCloseSnackbar = () => {
    //setOpenSnackbar(false);
  };

  // Helper function to format pricing period
  const formatPricingPeriod = (period) => {
    if (period === 7) {
      return '7 days'; // Replace 7 with "7 days"
    } else if (period === 30) {
      return '30 days'; // Replace 30 with "30 days"
    }
    return period;
  };
// Function to handle subscription
const handleSubscribe = (planId, pricingId) => {
  axios.post('https://backend.grabbereat.com/create_stripe_session', {
    plan_id: planId,
    pricing_id: pricingId,
    username: username
  })
  .then((response) => {
    if (response.data.session_url) {
      // Redirect the user to Stripe
      window.location.href = response.data.session_url;
    } else {
      console.error('Unexpected response:', response.data);
    }
  })
  .catch((error) => {
    console.error('Error creating Stripe session:', error);
  });
};

  // Helper function to get emoji based on quota value
  const getQuotaStatus = (value) => {
    return value === 1 ? '✅' : '❌';
  };

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ display: 'flex', minHeight: '100vh', backgroundColor: '#121212' }}>
        <Box sx={{ flexGrow: 1, paddingLeft: 3 }}>
          <Container maxWidth="lg" sx={{ paddingTop: 4 }}>
            <Typography color="white" marginTop="50px" variant="h4" gutterBottom>
              Membership Plans
            </Typography>

            {/* Display the plans */}
            <Grid container spacing={3}>
              {plans.length > 0 ? (
                plans.map((plan) => (
                  <Grid item xs={12} sm={6} md={4} key={plan.plan_id}>
                    <Card sx={{ backgroundColor: '#1c1c1c', color: 'white' }}>
                      <CardContent>
                        <Typography variant="h6" component="div">
                          {plan.plan_name}
                        </Typography>
                        <Typography variant="body2" color="textSecondary" gutterBottom>
                          {plan.plan_description}
                        </Typography>

                        {/* Display quotas */}
                        {plan.quotas && plan.quotas.length > 0 && (
                          <Box>
                            <Typography variant="subtitle1">Quotas:</Typography>
                            <List>
                              {plan.quotas.map((quota) => (
                                <ListItem key={quota.quota_id}>
                                  <ListItemText
                                    primary={`${quota.quota_name}: ${getQuotaStatus(quota.quota_value)}`}
                                    secondary={quota.quota_description}
                                  />
                                </ListItem>
                              ))}
                            </List>
                          </Box>
                        )}

                        <Divider sx={{ margin: '10px 0' }} />

                        {/* Display pricing */}
                        {plan.pricing && plan.pricing.length > 0 && (
                          <Box>
                            <Typography variant="subtitle1">Pricing:</Typography>
                            <List>
                              {plan.pricing.map((pricing) => (
                                <ListItem key={pricing.pricing_id}>
                                  <ListItemText
                                    primary={`${pricing.pricing_name} - £${pricing.price} (${formatPricingPeriod(pricing.pricing_period)})`}
                                    secondary={pricing.has_automatic_renewal ? 'Automatic Renewal: Yes' : 'Automatic Renewal: No'}
                                  />
                                  {/* Subscribe Button */}
                                  <Button
                                    variant="contained"
                                    color="primary"
                                    onClick={() => handleSubscribe(plan.plan_id, pricing.pricing_id)}
                                    sx={{ marginLeft: '10px' }}
                                  >
                                    Subscribe
                                  </Button>
                                </ListItem>
                              ))}
                            </List>
                          </Box>
                        )}
                      </CardContent>
                    </Card>
                  </Grid>
                ))
              ) : (
                <Typography variant="body1">No plans available at the moment.</Typography>
              )}
            </Grid>

            {/* Snackbar for notifications */}
            <Snackbar
              open={openSnackbar}
              message={message}
              autoHideDuration={3000}
              onClose={handleCloseSnackbar}
            />
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default MembershipPlans;
