import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import {
  Container, Box, Typography, TextField, Button, Grid, Paper,
  Snackbar, Alert, Link
} from '@mui/material';
import axios from 'axios';

// Dark theme configuration
const theme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const SupportPage = () => {
  const [formData, setFormData] = useState({ name: '', email: '', query: '' });
  const [openSnackbar, setOpenSnackbar] = useState(false);

  // Handle form data input change
  const handleFormChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };

  // Handle form submission
  const handleSubmitForm = async () => {
    if (formData.name && formData.email && formData.query) {
      try {
        const response = await axios.post('https://backend.grabbereat.com/send_support_email', formData);
        
        if (response.status === 200) {
          setOpenSnackbar(true);
          setFormData({ name: '', email: '', query: '' });
        }
      } catch (error) {
        console.error('Error sending email:', error);
        // Handle error (e.g., show a snackbar for error)
      }
    }
  };

  // Close snackbar
  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
  };

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="md" sx={{ paddingTop: 4 }}>
        <Typography variant="h4" gutterBottom textAlign="center">
          Support Center
        </Typography>

        <Paper sx={{ padding: 3, backgroundColor: 'background.paper' }}>
          <Typography color="white" marginTop="50px" variant="h6" gutterBottom>
            Submit a Support Ticket
          </Typography>

          {/* Support Ticket Form */}
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                label="Name"
                variant="outlined"
                fullWidth
                margin="normal"
                name="name"
                value={formData.name}
                onChange={handleFormChange}
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                label="Email"
                variant="outlined"
                fullWidth
                margin="normal"
                name="email"
                value={formData.email}
                onChange={handleFormChange}
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                label="Query"
                variant="outlined"
                fullWidth
                margin="normal"
                name="query"
                value={formData.query}
                onChange={handleFormChange}
                multiline
                rows={4}
              />
            </Grid>

            <Grid item xs={12}>
              <Button
                variant="contained"
                color="primary"
                onClick={handleSubmitForm}
                fullWidth
              >
                Submit Ticket
              </Button>
            </Grid>
          </Grid>

          {/* WhatsApp Support Link */}
          <Box sx={{ marginTop: 3, textAlign: 'center' }}>
            <Typography variant="body1" color="white">
              For urgent support, you can also contact us on WhatsApp at{' '}
              <Link href="https://wa.me/447424931877" target="_blank" color="primary">
                +44 7424 931877
              </Link>
              .
            </Typography>
          </Box>
        </Paper>

        {/* Snackbar for confirmation */}
        <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={handleCloseSnackbar}>
          <Alert onClose={handleCloseSnackbar} severity="success" sx={{ width: '100%' }}>
            Your support ticket has been submitted successfully!
          </Alert>
        </Snackbar>
      </Container>
    </ThemeProvider>
  );
};

export default SupportPage;
