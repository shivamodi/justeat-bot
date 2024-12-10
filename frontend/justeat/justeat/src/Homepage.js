import React, { useState } from 'react';
import styled, { createGlobalStyle } from 'styled-components';
import { AppBar, Box, Button, Container, Grid, IconButton, Toolbar, Typography, Paper, Accordion, AccordionSummary, AccordionDetails, TextField, ThemeProvider, createTheme } from '@mui/material';
import { ChevronLeft, ExpandMore } from '@mui/icons-material';
import FAQSection from './FaqSection';
import Footer from './Footer';
// Global styles for Dark Mode and Poppins font
const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  body {
    font-family: 'Poppins', sans-serif;
    background-color: #121212;
    color: #fff;
  }
  
  a {
    text-decoration: none;
  }
`;

// Material UI Dark Theme
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#1976d2', // ShiftGenie-like blue for primary button
    },
    secondary: {
      main: '#424242', // Darker gray for secondary actions (like outline)
    },
    background: {
      default: '#121212', // Dark background
      paper: '#1e1e1e', // Slightly lighter for paper-like surfaces
    },
    text: {
      primary: '#fff', // White text
      secondary: '#b0bec5', // Light gray for secondary text
    },
  },
  typography: {
    fontFamily: 'Poppins, sans-serif',
  },
});

// Styled components
const StyledAppBar = styled(AppBar)`
  background-color: #1e1e1e;
  box-shadow: none;
`;

const StyledToolbar = styled(Toolbar)`
  display: flex;
  justify-content: space-between;
`;

const Logo = styled.img`
  width: 50px;
  height: auto;
`;

const ButtonGroup = styled(Box)`
  display: flex;
  gap: 1rem;
`;

const StyledContainer = styled(Container)`
  margin-top: 80px;
`;

const StyledGrid = styled(Grid)`
  gap: 2rem;
`;

const StyledCard = styled(Paper)`
  background-color: #1e1e1e;
  padding: 16px;
  box-shadow: none;
`;

const CardText = styled(Typography)`
  color: #b0bec5;
`;

const ContactForm = styled.form`
  margin-top: 3rem;
`;

const SubmitButton = styled(Button)`
  background-color: #1976d2;
  color: white;
  margin-top: 1rem;
`;

const StyledAccordion = styled(Accordion)`
  background-color: #1e1e1e;
  border: none;
  margin-bottom: 1rem;
  box-shadow: none;
`;

const StyledAccordionSummary = styled(AccordionSummary)`
  background-color: #333;
  color: white;
`;

const StyledAccordionDetails = styled(AccordionDetails)`
  background-color: #222;
  color: #b0bec5;
`;

function Homepage() {
  const [expanded, setExpanded] = useState(false);

  const handleChange = (panel) => (event, newExpanded) => {
    setExpanded(newExpanded ? panel : false);
  };

  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <StyledAppBar position="fixed">
        <StyledToolbar>
          <IconButton edge="start" color="inherit" aria-label="menu">
            <ChevronLeft />
          </IconButton>
          <Logo src="/static/media/logo.png" alt="Logo" />
          <Box sx={{ flexGrow: 1 }} />
          <ButtonGroup>
            <Button color="inherit">Home</Button>
            <Button href="/signin" variant="outlined" color="inherit">Sign-in</Button>
            <Button href="/signup" variant="contained" color="primary">Sign-up</Button>
          </ButtonGroup>
        </StyledToolbar>
      </StyledAppBar>

      <StyledContainer>
        <StyledGrid container spacing={4}>
          {/* Text and CTA Section */}
          <StyledGrid item xs={12} lg={6}>
            <Typography variant="body1" gutterBottom>Try completely free for 3 days</Typography>
            <Typography variant="h3" gutterBottom>Fully automated Open Run grabber</Typography>
            <Typography variant="body1" paragraph>
              Are you tired of spending precious time searching for open runs that match your availability? GrabberEat is here to help! Let us take on the burden of finding open runs that perfectly align with your schedule.
            </Typography>
            <ButtonGroup>
              <Button  href="/signup" variant="contained" size="large" color="primary">Try Free</Button>
              <Button  href="/signin" variant="outlined" size="large" color="secondary">Sign-in</Button>
            </ButtonGroup>
            <CardText variant="caption">* No billing information required</CardText>
          </StyledGrid>

          {/* Hero Image Section */}
          <StyledGrid item xs={12} lg={5}>

          </StyledGrid>
        </StyledGrid>

        {/* FAQ Section with Accordion */}
        <FAQSection />

        {/* Contact Us Section */}
        <Box sx={{ marginTop: 8 }}>
          <Typography variant="h4">Contact Us</Typography>
          <ContactForm>
            <Grid container spacing={2}>
              <Grid item xs={12} lg={6}>
                <TextField fullWidth label="Full Name" variant="filled" color="primary" />
                <TextField fullWidth label="Email Address" variant="filled" color="primary" sx={{ marginTop: 2 }} />
                <TextField fullWidth label="Phone Number" variant="filled" color="primary" sx={{ marginTop: 2 }} />
              </Grid>
              <Grid item xs={12} lg={6}>
                <TextField
                  fullWidth
                  label="Question"
                  variant="filled"
                  color="primary"
                  multiline
                  rows={4}
                  sx={{ marginTop: 2 }}
                />
              </Grid>
            </Grid>
            <SubmitButton variant="contained" size="large" color="primary">Submit</SubmitButton>
          </ContactForm>
        </Box>
      </StyledContainer>
      <Footer />
    </ThemeProvider>
  );
}

export default Homepage