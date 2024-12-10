import React, { useEffect, useState } from "react";
import { Container, Typography, Paper, Grid, Card, CardContent, Box, CircularProgress, Button, List, ListItem, ListItemText, Divider, IconButton } from "@mui/material";
import { FileCopy as FileCopyIcon } from '@mui/icons-material';
import axios from 'axios';
import Cookies from 'js-cookie';
import { FacebookShareButton, TwitterShareButton, EmailShareButton, FacebookIcon, TwitterIcon, EmailIcon } from "react-share";

const ReferralPage = () => {
  const [referrals, setReferrals] = useState([]);
  const [referralCounts, setReferralCounts] = useState({
    basic_weekly: [],
    basic_monthly: [],
    premium_weekly: [],
    premium_monthly: []
  });
  const [awardedPlans, setAwardedPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const username = localStorage.getItem('userName');

  const handleSubmit = () => {
    const csrftoken = Cookies.get('csrftoken');

    axios.post('https://backend.grabbereat.com/get_referrals', {
      username: username
    }, {
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      setReferrals(response.data.referrals);
      setLoading(false);
    })
    .catch(error => {
      setError(error.message);
      setLoading(false);
    });
  };

  const fetchReferralCounts = async () => {
    try {
      const csrftoken = Cookies.get('csrftoken');

      const response = await axios.post('https://backend.grabbereat.com/get_referral_counts', {
        username: username
      }, {
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json'
        }
      });

      if (
        response.data.basic_weekly &&
        response.data.basic_monthly &&
        response.data.premium_weekly &&
        response.data.premium_monthly
      ) {
        setReferralCounts(response.data);
      } else {
        setReferralCounts({
          basic_weekly: [],
          basic_monthly: [],
          premium_weekly: [],
          premium_monthly: []
        });
      }
    } catch (err) {
      setError("Unable to fetch referral counts.");
    }
  };

  const fetchAwardedPlans = async () => {
    try {
      const csrftoken = Cookies.get('csrftoken');

      const response = await axios.post('https://backend.grabbereat.com/get_awarded_plans', {
        username: username
      }, {
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json'
        }
      });

      setAwardedPlans(Object.values(response.data.awarded_plans));
    } catch (err) {
      setError("Unable to fetch awarded plans.");
    }
  };

  const handleClaimPlan = (planName, pricingId) => {
    const csrftoken = Cookies.get('csrftoken');

    axios.post('https://backend.grabbereat.com/claim_plan', {
      username: username,
      plan_name: planName,
      pricing_id: pricingId
    }, {
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      fetchAwardedPlans();
    })
    .catch(error => {
      console.error('Error claiming plan:', error);
    });
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      alert("Copied to clipboard!");
    }).catch(err => {
      console.error('Error copying text: ', err);
    });
  };

  useEffect(() => {
    handleSubmit();
    fetchReferralCounts();
    fetchAwardedPlans();
  }, [username]);

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh", backgroundColor: '#121212' }}>
        <CircularProgress color="primary" />
      </Box>
    );
  }

  if (error) {
    return (
      <Container sx={{ backgroundColor: '#121212', color: '#ffffff' }}>
        <Typography variant="h6" color="error">
          Error: {error}
        </Typography>
      </Container>
    );
  }

  const getPricingLabel = (pricingId) => {
    return pricingId === 1 ? 'Weekly' : 'Monthly';
  };

  return (
    <Container maxWidth="md" sx={{ marginTop: 5, backgroundColor: '#121212', color: '#ffffff', padding: { xs: 2, md: 5 } }}>
      <Typography variant="h4" marginTop="50px" color="white" gutterBottom>
        Referral Responses
      </Typography>

      {referralCounts.basic_weekly.length !== 0 && (
        <>
          <Typography variant="h5" marginTop="20px" color="white" gutterBottom>
            Basic Plan Referral Counts (Weekly)
          </Typography>
          <Paper elevation={3} sx={{ backgroundColor: '#1E1E1E', padding: 2, borderRadius: 2, marginBottom: 3 }}>
            <List>
              {referralCounts.basic_weekly.map((count, index) => (
                <ListItem key={index}>
                  <ListItemText primary={`${count.user__username}: ${count.count}`} sx={{ color: 'white' }} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </>
      )}

      {referralCounts.basic_monthly.length !== 0 && (
        <>
          <Typography variant="h5" marginTop="20px" color="white" gutterBottom>
            Basic Plan Referral Counts (Monthly)
          </Typography>
          <Paper elevation={3} sx={{ backgroundColor: '#1E1E1E', padding: 2, borderRadius: 2, marginBottom: 3 }}>
            <List>
              {referralCounts.basic_monthly.map((count, index) => (
                <ListItem key={index}>
                  <ListItemText primary={`${count.user__username}: ${count.count}`} sx={{ color: 'white' }} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </>
      )}

      {referralCounts.premium_weekly.length !== 0 && (
        <>
          <Typography variant="h5" marginTop="20px" color="white" gutterBottom>
            Premium Plan Referral Counts (Weekly)
          </Typography>
          <Paper elevation={3} sx={{ backgroundColor: '#1E1E1E', padding: 2, borderRadius: 2, marginBottom: 3 }}>
            <List>
              {referralCounts.premium_weekly.map((count, index) => (
                <ListItem key={index}>
                  <ListItemText primary={`${count.user__username}: ${count.count}`} sx={{ color: 'white' }} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </>
      )}

      {referralCounts.premium_monthly.length !== 0 && (
        <>
          <Typography variant="h5" marginTop="20px" color="white" gutterBottom>
            Premium Plan Referral Counts (Monthly)
          </Typography>
          <Paper elevation={3} sx={{ backgroundColor: '#1E1E1E', padding: 2, borderRadius: 2, marginBottom: 3 }}>
            <List>
              {referralCounts.premium_monthly.map((count, index) => (
                <ListItem key={index}>
                  <ListItemText primary={`${count.user__username}: ${count.count}`} sx={{ color: 'white' }} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </>
      )}

      {referrals.length === 0 ? (
        <Typography variant="body1" color="white">
          No referrals yet.
        </Typography>
      ) : (
        referrals.map((referral, index) => {
          const referralLink = `https://grabbereat.com/referrals/${referral.referral_code}`;
          return (
            <Grid item xs={12} sm={12} md={12} key={index}>
              <Paper elevation={3} sx={{
                backgroundColor: '#1E1E1E', // Dark card background
                padding: 2,
                borderRadius: 2,
                marginBottom: 3
              }}>
                <Card sx={{ backgroundColor: '#121212' }}>
                  <CardContent>
                    <Typography variant="h6" color="white">
                      Invite Two Friends Today to Unlock a Free Package
                    </Typography>

                    <Typography variant="h6" color="white" sx={{ mt: 3 }}>
                      Share your referral link:
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', overflowX: 'auto', whiteSpace: 'nowrap', backgroundColor: '#2E2E2E', padding: '10px', borderRadius: '5px', mb: 3, maxWidth: '100%' }}>
                    <Typography variant="body1" color="white" sx={{ display: 'inline', mr: 2 }}>
                        Copy Link
                      </Typography>
                      <IconButton color="primary" onClick={() => copyToClipboard(referralLink)}>
                        <FileCopyIcon />
                      </IconButton>
                    </Box>

                    <Box sx={{ display: "flex", gap: 2, mb: 3 }}>
                      <FacebookShareButton url={referralLink}>
                        <FacebookIcon size={32} round />
                      </FacebookShareButton>
                      <TwitterShareButton url={referralLink}>
                        <TwitterIcon size={32} round />
                      </TwitterShareButton>
                      <EmailShareButton url={referralLink} subject="Join me on Grabbereat!" body={`Use my referral link to join: ${referralLink}`}>
                        <EmailIcon size={32} round />
                      </EmailShareButton>
                    </Box>
                  </CardContent>
                </Card>
              </Paper>
            </Grid>
          );
        })
      )}

      {/* Display awarded plans with claim buttons */}
      {awardedPlans.length > 0 && (  
  <Container sx={{ marginTop: '50px', backgroundColor: '#1E1E1E', padding: '20px', borderRadius: '8px' }}>  
    <Typography variant="h4" color="white" gutterBottom>  
      Awarded Free Plans  
    </Typography>  
    {awardedPlans.map((plan, index) => {  
      const freePlansAvailable = Math.floor(plan.free_plans_to_award / 2); // Assuming this is the total available  
      const claimedCount = Math.floor(plan.claimed_count); // Assuming claimed_count is an integer field in the model  

      return (  
        <Box key={index} sx={{ marginBottom: '20px', padding: '20px', backgroundColor: '#2c2c2c', borderRadius: '5px' }}>  
          <Typography variant="body1" color="white">  
            Plan: {plan.plan_name}<br/>   
            Pricing: {index % 2 === 0 ? 'WEEKLY' : 'MONTHLY'}<br/>   
            Referral Count: {plan.free_plans_to_award ? plan.free_plans_to_award : 0 }<br/>   
            Free Plans Available: {freePlansAvailable}<br />   
            Free Plans Claimed: {claimedCount}  
          </Typography>  
          <Button   
            variant="contained"   
            color="primary"   
            sx={{  
              marginTop: '10px',  
              '&.Mui-disabled': {  
                backgroundColor: '#B0BEC5',  
                color: 'white'  
              }  
            }}  
            onClick={() => handleClaimPlan(plan.plan_name, plan.pricing_id)}  
            disabled={freePlansAvailable <= claimedCount} // Disable if claimed count is equal to or greater than available  
          >  
            Claim Free Plan  
          </Button>  
        </Box>  
      );  
    })}  
  </Container>  
)}  
    </Container>
  );
};

export default ReferralPage;
