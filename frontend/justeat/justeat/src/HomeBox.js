import React from 'react';
import { Box, Container, Grid, Typography, Button } from '@mui/material';

export default function HomeBox() {
  return (
    <Box>
      <Container>
        <Grid container>
          <Grid item xs={12} lg={6}>
            <Box>
              <Typography variant="body1">Try completely free for 7 days</Typography>
              <Typography variant="h3">Fully automated Open Run grabber</Typography>
              <Typography variant="body1">
                Are you tired of spending precious time searching for open runs that match your availability? 
                Shift Genie is here to help! Let us take on the burden of finding open runs that perfectly align 
                with your schedule.
              </Typography>
              <Box>
                <Button variant="contained" color="primary" size="large" href="/signUp">Try Free</Button>
                <Button variant="outlined" color="primary" size="large" href="/signIn">Sign-in</Button>
              </Box>
              <Typography variant="caption">* No billing information required</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} lg={6}>
            <img alt="Shift Genie App Preview" src="/static/media/phoneMockup.85c06ff26fd2075dece6.webp" />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}
