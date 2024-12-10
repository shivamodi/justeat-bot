import { Button, Container, Grid, TextField, Typography, Box, Link, Snackbar } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import styled from 'styled-components';
import axios from 'axios';
import React, { useState } from 'react';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';

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

const SignInContainer = styled(Container)`
  margin-top: 100px;
`;

const SignInForm = styled(Box)`
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

function SignIn() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [forgotPasswordEmail, setForgotPasswordEmail] = useState('');
  const [forgotPasswordError, setForgotPasswordError] = useState('');
  const [showForgotPasswordForm, setShowForgotPasswordForm] = useState(false);  // New state to toggle form
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();

    // Get CSRF token if needed
    const csrftoken = Cookies.get('csrftoken');
    axios.post('https://backend.grabbereat.com/login_view', {
      username: username,
      password: password
    }, {
      headers: {
        'X-CSRFToken': csrftoken,  // Include CSRF token in the request headers
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      console.log('Login successful:', response.data);
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('userName');
      localStorage.removeItem('email');
      localStorage.removeItem('justEatCredentials');
      localStorage.removeItem('currentPlan');
      localStorage.removeItem('firstname');
      localStorage.removeItem('lastname');
      localStorage.removeItem('open_runs_toggle');
      localStorage.removeItem('overflows_toggle');
      // Handle successful login (e.g., redirect or update UI)
      localStorage.setItem('isAuthenticated', response.data.userAuthenticated);
      localStorage.setItem('userName', response.data.request.id);
      localStorage.setItem('email', response.data.request.email);
      localStorage.setItem('firstname', response.data.request.firstname);
      localStorage.setItem('lastname', response.data.request.lastname);
      localStorage.setItem('justEatCredentials', JSON.stringify(response.data.request.justEatCredentials));
      localStorage.setItem('open_runs_toggle', response.data.request.open_runs_toggle);
      localStorage.setItem('overflows_toggle', response.data.request.overflows_toggle);
      localStorage.setItem('currentPlan', JSON.stringify(response.data.request.currentPlan));
      setSnackbarMessage('Login successful!');
      setOpenSnackbar(true);
      navigate('/dash');
    })
    .catch(error => {
      console.error('Error logging in:', error);
      // Handle error (e.g., show error message)
      setSnackbarMessage('Error: Invalid Credentials');
      setOpenSnackbar(true);
    });
  };

  const handleForgotPasswordSubmit = (event) => {
    event.preventDefault();

    // Get CSRF token if needed
    const csrftoken = Cookies.get('csrftoken');
    axios.post('https://backend.grabbereat.com/forgot_password', {
      email: forgotPasswordEmail,
    }, {
      headers: {
        'X-CSRFToken': csrftoken,  // Include CSRF token in the request headers
        'Content-Type': 'application/json',
      }
    })
    .then(response => {
      console.log('Password reset request sent:', response.data);
      setSnackbarMessage('Password reset link has been sent to your email!');
      setOpenSnackbar(true);
      setShowForgotPasswordForm(false);  // Hide form after submission
    })
    .catch(error => {
      console.error('Error in password reset request:', error);
      setForgotPasswordError('Failed to send reset link: ' + error.message);
    });
  };

  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
  };

  return (
    <ThemeProvider theme={theme}>
      <SignInContainer>
        <Grid container justifyContent="center">
          <Grid item xs={12} sm={8} md={6} lg={4}>
            <SignInForm>
              <FormTitle variant="h5">Sign In to Your Account</FormTitle>
              <TextField
                fullWidth
                name="username"
                label="Email Address"
                variant="filled"
                color="primary"
                margin="normal"
                type="email"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <TextField
                fullWidth
                name="password"
                label="Password"
                variant="filled"
                color="primary"
                margin="normal"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <Button
                fullWidth
                variant="contained"
                color="primary"
                size="large"
                sx={{ marginTop: 2 }}
                onClick={handleSubmit}
              >
                Sign In
              </Button>

              {/* Forgot Password Link */}
              <Box sx={{ marginTop: 2, textAlign: 'center' }}>
                <Typography variant="body2" color="text.secondary">
                  Forgot your password?{' '}
                  <Link href="#" onClick={() => setShowForgotPasswordForm(true)}>
                    Reset it
                  </Link>
                </Typography>
              </Box>

              {/* Forgot Password Form */}
              {showForgotPasswordForm && (
                <Box sx={{ marginTop: 3 }}>
                  <TextField
                    fullWidth
                    label="Enter your email address"
                    variant="filled"
                    color="primary"
                    margin="normal"
                    type="email"
                    value={forgotPasswordEmail}
                    onChange={(e) => setForgotPasswordEmail(e.target.value)}
                  />
                  <Button
                    fullWidth
                    variant="contained"
                    color="primary"
                    size="large"
                    sx={{ marginTop: 2 }}
                    onClick={handleForgotPasswordSubmit}
                  >
                    Send Reset Link
                  </Button>
                  {forgotPasswordError && (
                    <Typography color="error" variant="body2" align="center">
                      {forgotPasswordError}
                    </Typography>
                  )}
                </Box>
              )}

              <Box sx={{ marginTop: 2, textAlign: 'center' }}>
                <Typography variant="body2" color="text.secondary">
                  Don't have an account? <Link href="/signUp">Sign up</Link>
                </Typography>
              </Box>
            </SignInForm>
          </Grid>
        </Grid>

        {/* Snackbar for showing success or error messages */}
        <Snackbar
          open={openSnackbar}
          autoHideDuration={3000}
          onClose={handleCloseSnackbar}
          message={snackbarMessage}
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
          severity={error ? 'error' : 'success'}
        />
      </SignInContainer>
    </ThemeProvider>
  );
}

export default SignIn;
