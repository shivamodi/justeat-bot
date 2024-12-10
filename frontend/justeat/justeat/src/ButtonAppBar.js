import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';

export default function ButtonAppBar() {
    const appbarstyle = { backgroundColor: '#1E1F24' };
    const buttonstyle1 = { borderRadius: 0, color: '#78ede3' };
    const buttonstyle2 = { borderRadius: 0, backgroundColor: '#78ede3' };
    const buttonstyle3 = { borderRadius: 0 };
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar style={appbarstyle} position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Home
          </Typography>
          <Button href="/" sx={{ marginX: 2 }} style={buttonstyle1} variant="text" color="inherit">HOME</Button>
          <Button href="/login" sx={{ marginX: 2 }} style={buttonstyle3} variant="outlined" color="inherit">SIGN IN</Button>
          <Button href="/register"  sx={{ marginX: 2 }} style={buttonstyle2} variant="contained" color="inherit">SIGNUP</Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}