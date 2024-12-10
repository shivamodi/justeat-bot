import React, { useState, useEffect } from 'react';
import { Button, Container, Grid, TextField, Typography, Box, Link } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import styled from 'styled-components';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Snackbar, Alert } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';  // For navigation and accessing URL

// Material UI Dark Theme
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#1976d2', // ShiftGenie-like blue for primary button
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

const SignUpContainer = styled(Container)`
  margin-top: 100px;
`;

const SignUpForm = styled(Box)`
  background-color: #1e1e1e;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
`;

const FormTitle = styled(Typography)`
  text-align: center;
  margin-bottom: 20px;
  color: #fff;
`;

const SignUp = () => {
  const [formData, setFormData] = useState({
    fullname: '',
    email: '',
    password: '',
    confirm_password: '',
    mobile: '',
  });

  const [message, setMessage] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [severity, setSeverity] = useState('success');
  const [userIp, setUserIp] = useState(null); // Store the user's IP address
  const [referralCode, setReferralCode] = useState(null); // Store the referral code from the URL

  const navigate = useNavigate();
  const location = useLocation(); // To access URL query params or path

  // Fetch user IP address from an external service
  const fetchUserIp = async () => {
    try {
      const response = await axios.get('https://api.ipify.org?format=json');
      setUserIp(response.data.ip);
    } catch (error) {
      console.error('Error fetching IP address:', error);
    }
  };

  // Extract referral code from the URL (using location.pathname or location.search if it's in query params)
  const extractReferralCode = () => {
    const pathParts = location.pathname.split('/');
    const referral = pathParts[pathParts.length - 1]; // Assuming referral code is at the end of the URL
    setReferralCode(referral);
  };

  // Handle form field changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  // Handle form submit
  const handleSubmit = (e) => {
    e.preventDefault();

    // Simple client-side validation
    if (!formData.fullname || !formData.email || !formData.password || !formData.confirm_password || !formData.mobile) {
      setMessage('All fields are required.');
      setOpenSnackbar(true);
      return;
    }

    if (formData.password !== formData.confirm_password) {
      setMessage('Passwords do not match.');
      setOpenSnackbar(true);
      return;
    }

    // Get CSRF token if needed
    const csrftoken = Cookies.get('csrftoken');

    // Axios POST request for registration
    axios
      .post('https://backend.grabbereat.com/register', {
        username: formData.fullname,
        email: formData.email,
        password: formData.password,
        confirmation: formData.confirm_password,
        mobile: formData.mobile,
      }, {
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json',
        },
      })
      .then((response) => {
        console.log('Successful:', response.data);
        setMessage('Registration successful!');
        setSeverity('success');
        setOpenSnackbar(true);

        // After successful registration, send referral details (IP, session key, and referral code) to the backend
        const sessionKey = sessionStorage.getItem('sessionKey'); // Retrieve session key from sessionStorage

        if (sessionKey && userIp && referralCode) {
          axios
            .post('https://backend.grabbereat.com/record_signup', {
              referral_code: referralCode,
              session_key: sessionKey,
              user_ip: userIp,
              username: formData.email,
            })
            .then((response) => {
              console.log('Referral record updated:', response.data);
            })
            .catch((error) => {
              console.error('Error recording referral:', error);
            });
        }

        // Redirect to login page after successful registration
        setTimeout(() => {
          navigate('/signin');
        }, 3000);
      })
      .catch((error) => {
        console.error('Error during registration:', error);

        let errorMessage = 'An error occurred. Please try again later.';
        let severity = 'error';

        if (error.response) {
          errorMessage = error.response.data.message || 'An error occurred. Please try again later.';
        }

        setMessage(errorMessage);
        setSeverity(severity);
        setOpenSnackbar(true);
      });
  };

  // Fetch user IP and referral code when the component mounts
  useEffect(() => {
    fetchUserIp(); // Fetch IP address
    extractReferralCode(); // Extract referral code from the URL
  }, []); // Empty array means this effect runs only once when the component mounts

  return (
    <ThemeProvider theme={theme}>
      <SignUpContainer>
        <Grid container justifyContent="center">
          <Grid item xs={12} sm={8} md={6} lg={4}>
            <SignUpForm>
              <FormTitle variant="h5">Create Your Account</FormTitle>
              <TextField
                fullWidth
                label="Full Name"
                variant="filled"
                color="primary"
                margin="normal"
                name="fullname"
                value={formData.fullname}
                onChange={handleInputChange}
              />
              <TextField
                fullWidth
                label="Email Address"
                variant="filled"
                color="primary"
                margin="normal"
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
              />
              <TextField
                fullWidth
                label="Password"
                variant="filled"
                color="primary"
                margin="normal"
                type="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
              />
              <TextField
                fullWidth
                label="Confirm Password"
                variant="filled"
                color="primary"
                margin="normal"
                type="password"
                name="confirm_password"
                value={formData.confirm_password}
                onChange={handleInputChange}
              />
              <TextField
                fullWidth
                label="Mobile Number"
                variant="filled"
                color="primary"
                margin="normal"
                name="mobile"
                value={formData.mobile}
                onChange={handleInputChange}
              />
              <Button
                fullWidth
                variant="contained"
                color="primary"
                size="large"
                sx={{ marginTop: 2 }}
                onClick={handleSubmit}
              >
                Sign Up
              </Button>
              <Box sx={{ marginTop: 2, textAlign: 'center' }}>
                <Typography variant="body2" color="text.secondary">
                  Already have an account? <Link href="/signin">Sign in</Link>
                </Typography>
              </Box>
            </SignUpForm>
          </Grid>
        </Grid>

        {/* Snackbar for success/error messages */}
        <Snackbar
          open={openSnackbar}
          autoHideDuration={3000}
          onClose={() => setOpenSnackbar(false)}
        >
          <Alert
            onClose={() => setOpenSnackbar(false)}
            severity={severity}
            sx={{ width: '100%' }}
          >
            {message}
          </Alert>
        </Snackbar>
      </SignUpContainer>
    </ThemeProvider>
  );
};

export default SignUp;
