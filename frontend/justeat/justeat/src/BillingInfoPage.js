import React, { useState } from 'react';
import { Container, Typography, TextField, Button, Snackbar, Box } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const theme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const BillingInfoPage = () => {
  const [billingInfo, setBillingInfo] = useState({
    tax_number: '',
    name: '',
    street: '',
    zipcode: '',
    city: '',
    country: '',
    shipping_name: '',
    shipping_street: '',
    shipping_zipcode: '',
    shipping_city: '',
  });
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const navigate = useNavigate();

  const username = localStorage.getItem('userName'); // Assuming user ID is saved in local storage

  const handleChange = (e) => {
    const { name, value } = e.target;
    setBillingInfo((prevInfo) => ({
      ...prevInfo,
      [name]: value,
    }));
  };

  const validate = () => {
    let tempErrors = {};
    tempErrors.tax_number = billingInfo.tax_number ? "" : "This field is required.";
    tempErrors.name = billingInfo.name ? "" : "This field is required.";
    tempErrors.street = billingInfo.street ? "" : "This field is required.";
    tempErrors.zipcode = billingInfo.zipcode ? "" : "This field is required.";
    tempErrors.city = billingInfo.city ? "" : "This field is required.";
    tempErrors.country = billingInfo.country ? "" : "This field is required.";
    setErrors(tempErrors);
    return Object.values(tempErrors).every(x => x === "");
  };

  const handleSubmit = () => {
    if (validate()) {
      axios.post('https://backend.grabbereat.com/save_billing_info', {
        username: username,
        ...billingInfo,
      })
      .then((response) => {
        if (response.data.status === 'success') {
          setMessage('Billing info saved successfully');
          setOpenSnackbar(true);
          navigate('/membership');
        } else {
          setMessage('Failed to save billing info');
          setOpenSnackbar(true);
        }
      })
      .catch((error) => {
        console.error('Error saving billing info:', error);
        setMessage('Failed to save billing info');
        setOpenSnackbar(true);
      });
    } else {
      setMessage('Please fill all required fields');
      setOpenSnackbar(true);
    }
  };

  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
  };

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="sm" sx={{ paddingTop: 4 }}>
        <Typography variant="h4" color="white" gutterBottom>
          Billing Information
        </Typography>
        <Box component="form" noValidate autoComplete="off">
          <TextField
            label="Tax Number"
            variant="filled"
            name="tax_number"
            fullWidth
            margin="normal"
            value={billingInfo.tax_number}
            onChange={handleChange}
            sx={{ backgroundColor: '#1c1c1c', color: 'white' }}
            error={!!errors.tax_number}
            helperText={errors.tax_number}
          />
          <TextField
            label="Name"
            variant="filled"
            name="name"
            fullWidth
            margin="normal"
            value={billingInfo.name}
            onChange={handleChange}
            sx={{ backgroundColor: '#1c1c1c', color: 'white' }}
            error={!!errors.name}
            helperText={errors.name}
          />
          <TextField
            label="Street"
            variant="filled"
            name="street"
            fullWidth
            margin="normal"
            value={billingInfo.street}
            onChange={handleChange}
            sx={{ backgroundColor: '#1c1c1c', color: 'white' }}
            error={!!errors.street}
            helperText={errors.street}
          />
          <TextField
            label="Zipcode"
            variant="filled"
            name="zipcode"
            fullWidth
            margin="normal"
            value={billingInfo.zipcode}
            onChange={handleChange}
            sx={{ backgroundColor: '#1c1c1c', color: 'white' }}
            error={!!errors.zipcode}
            helperText={errors.zipcode}
          />
          <TextField
            label="City"
            variant="filled"
            name="city"
            fullWidth
            margin="normal"
            value={billingInfo.city}
            onChange={handleChange}
            sx={{ backgroundColor: '#1c1c1c', color: 'white' }}
            error={!!errors.city}
            helperText={errors.city}
          />
          <TextField
            label="Country"
            variant="filled"
            name="country"
            fullWidth
            margin="normal"
            value={billingInfo.country}
            onChange={handleChange}
            sx={{ backgroundColor: '#1c1c1c', color: 'white' }}
            error={!!errors.country}
            helperText={errors.country}
          />
          <TextField
            label="Shipping Name"
            variant="filled"
            name="shipping_name"
            fullWidth
            margin="normal"
            value={billingInfo.shipping_name}
            onChange={handleChange}
            sx={{ backgroundColor: '#1c1c1c', color: 'white' }}
          />
          <TextField
            label="Shipping Street"
            variant="filled"
            name="shipping_street"
            fullWidth
            margin="normal"
            value={billingInfo.shipping_street}
            onChange={handleChange}
            sx={{ backgroundColor: '#1c1c1c', color: 'white' }}
          />
          <TextField
            label="Shipping Zipcode"
            variant="filled"
            name="shipping_zipcode"
            fullWidth
            margin="normal"
            value={billingInfo.shipping_zipcode}
            onChange={handleChange}
            sx={{ backgroundColor: '#1c1c1c', color: 'white' }}
          />
          <TextField
            label="Shipping City"
            variant="filled"
            name="shipping_city"
            fullWidth
            margin="normal"
            value={billingInfo.shipping_city}
            onChange={handleChange}
            sx={{ backgroundColor: '#1c1c1c', color: 'white' }}
          />
          <Box textAlign="center" sx={{ marginTop: 2 }}>
            <Button variant="contained" color="primary" onClick={handleSubmit}>
              Save Billing Info
            </Button>
          </Box>
        </Box>
        <Snackbar
          open={openSnackbar}
          message={message}
          autoHideDuration={3000}
          onClose={handleCloseSnackbar}
        />
      </Container>
    </ThemeProvider>
  );
};

export default BillingInfoPage;
