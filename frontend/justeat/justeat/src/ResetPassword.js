import React, { useState, useEffect } from 'react';
import { Button, Container, Grid, TextField, Typography, Box, Snackbar } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import styled from 'styled-components';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';

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

const ResetPasswordContainer = styled(Container)`
  margin-top: 100px;
`;

const ResetPasswordForm = styled(Box)`
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

function ResetPassword() {
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();
  const { uid, token } = useParams(); // The token is passed via URL parameters

  const handleResetPassword = (event) => {
    event.preventDefault();

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      setOpenSnackbar(true);
      return;
    }

    setIsSubmitting(true);

    // Send the new password to the backend
    axios.post('https://backend.grabbereat.com/reset_password', {
      uid: uid,
      token: token, // Token from URL params
      new_password: newPassword,
    })
    .then((response) => {
      setMessage('Password reset successfully!');
      setOpenSnackbar(true);
      setTimeout(() => {
        navigate('/signin');  // Redirect to login page after successful password reset
      }, 3000);
    })
    .catch((error) => {
      setError('Failed to reset password: ' + error.response?.data?.message || error.message);
      setOpenSnackbar(true);
    })
    .finally(() => {
      setIsSubmitting(false);
    });
  };

  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
  };

  return (
    <ThemeProvider theme={theme}>
      <ResetPasswordContainer>
        <Grid container justifyContent="center">
          <Grid item xs={12} sm={8} md={6} lg={4}>
            <ResetPasswordForm>
              <FormTitle variant="h5">Reset Your Password</FormTitle>
              <TextField
                fullWidth
                label="New Password"
                variant="filled"
                color="primary"
                margin="normal"
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />
              <TextField
                fullWidth
                label="Confirm New Password"
                variant="filled"
                color="primary"
                margin="normal"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
              <Button
                fullWidth
                variant="contained"
                color="primary"
                size="large"
                sx={{ marginTop: 2 }}
                onClick={handleResetPassword}
                disabled={isSubmitting}
              >
                Reset Password
              </Button>

              {error && (
                <Typography color="error" variant="body2" align="center" sx={{ marginTop: 2 }}>
                  {error}
                </Typography>
              )}
            </ResetPasswordForm>
          </Grid>
        </Grid>

        <Snackbar
          open={openSnackbar}
          autoHideDuration={3000}
          onClose={handleCloseSnackbar}
          message={message || error}
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
          severity={error ? 'error' : 'success'}
        />
      </ResetPasswordContainer>
    </ThemeProvider>
  );
}

export default ResetPassword;
