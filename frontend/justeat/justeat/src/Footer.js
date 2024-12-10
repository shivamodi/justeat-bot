import React from 'react';
import { Box, Typography, IconButton, Grid, Container } from '@mui/material';
import { Facebook, Twitter, Instagram, LinkedIn } from '@mui/icons-material'; // Material UI Social Icons
import Logo from './logo.png'; // Replace with the actual path to your logo image

function Footer() {
  return (
    <Box sx={{ backgroundColor: '#212121', color: '#fff', py: 4 }}>
      <Container>
        <Grid container spacing={4} justifyContent="space-between" alignItems="center">
          {/* Logo Section */}
          <Grid item xs={12} md={4} textAlign="center">
            <img src={Logo} alt="GrabberEat Logo" style={{ width: '150px' }} />
            <Typography variant="body2" sx={{ mt: 2 }}>
              © 2024 GrabberEat. All rights reserved.
            </Typography>
          </Grid>

          {/* Social Links */}
          <Grid item xs={12} md={4} textAlign="center">
            <Typography variant="h6" sx={{ mb: 2 }}>
              Follow Us
            </Typography>
            <Box>
              <IconButton
                color="inherit"
                sx={{ mr: 2 }}
                href="https://www.facebook.com/shiftgenie"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Facebook />
              </IconButton>
              <IconButton
                color="inherit"
                sx={{ mr: 2 }}
                href="https://twitter.com/shiftgenie"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Twitter />
              </IconButton>
              <IconButton
                color="inherit"
                sx={{ mr: 2 }}
                href="https://www.instagram.com/shiftgenie"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Instagram />
              </IconButton>
              <IconButton
                color="inherit"
                href="https://www.linkedin.com/company/shiftgenie"
                target="_blank"
                rel="noopener noreferrer"
              >
                <LinkedIn />
              </IconButton>
            </Box>
          </Grid>

          {/* Additional Links (if any) */}
          <Grid item xs={12} md={4} textAlign="center">
            <Typography variant="body2" sx={{ mb: 1 }}>
              <a href="/terms" style={{ color: '#fff', textDecoration: 'none' }}>Terms & Conditions</a>
            </Typography>
            <Typography variant="body2">
              <a href="/privacy" style={{ color: '#fff', textDecoration: 'none' }}>Privacy Policy</a>
            </Typography>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default Footer;
