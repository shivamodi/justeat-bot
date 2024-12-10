import React, { useState, useEffect } from 'react';
import { Accordion, AccordionSummary, AccordionDetails, Switch, Typography, FormControlLabel, Box, Link, Modal, TextField, Button, CircularProgress } from '@mui/material';
import { ExpandMore } from '@mui/icons-material';
import { FaClipboardList, FaCalendarAlt, FaMapMarkerAlt } from 'react-icons/fa';
import { useSidebar } from './SidebarContext';
import axios from 'axios';
import Cookies from 'js-cookie';
import PowerSettingsNewIcon from '@mui/icons-material/PowerSettingsNew';
import StopIcon from '@mui/icons-material/Stop';
import { grey } from '@mui/material/colors';

const DashboardPage = () => {
  const isAuthenticated = localStorage.getItem('isAuthenticated');
  const username = localStorage.getItem('userName');
  const openRunsToggle = localStorage.getItem('open_runs_toggle');
  const overflowsToggle = localStorage.getItem('overflows_toggle');
  const { isDrawerOpen, isHamburgerVisible } = useSidebar();

  const [openRun, setOpenRun] = useState(openRunsToggle);
  const [overflows, setOverflows] = useState(overflowsToggle);
  const [currentPlan, setCurrentPlan] = useState(null);
  const [loadingPlan, setLoadingPlan] = useState(true);
  const [icon, setIcon] = useState('power');
  const [executionStatus, setExecutionStatus] = useState('stopped');
  const [loadingStatus, setLoadingStatus] = useState(false); // New state to handle loading status
  
  // Modal state for JustEat credentials
  const [openModal, setOpenModal] = useState(false);
  const [justEatUsername, setJustEatUsername] = useState('');
  const [justEatPassword, setJustEatPassword] = useState('');
  
  const justEatCredentials = localStorage.getItem('justEatCredentials');
  const justEat = JSON.parse(justEatCredentials);

  const handleOpenRunToggle = (event) => {
    const value = event.target.checked;
    setOpenRun(value);
    saveToggleValues({ open_run_toggle: value });
  };

  const handleOverflowsToggle = (event) => {
    const value = event.target.checked;
    setOverflows(value);
    saveToggleValues({ overflows_toggle: value });
  };

  const saveToggleValues = (toggles) => {
    const csrftoken = Cookies.get('csrftoken');
    axios.post('https://backend.grabbereat.com/save_toggle_values', {
      username: username,
      ...toggles
    }, {
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      console.log('Toggle values saved:', response.data);
    })
    .catch(error => {
      console.error('Error saving toggle values:', error);
    });
  };

  const handleClick = async (type) => {
    // Check if JustEat credentials are set
    const justEatCredentials = localStorage.getItem('justEatCredentials');
    const justEat = JSON.parse(justEatCredentials);
    
    // If credentials are not set, open the modal
    if (!justEatCredentials || !justEat.username || !justEat.password) {
      setOpenModal(true);
      return;
    }
  
    try {
      setLoadingStatus(true); // Start loading when fetching execution status
      const csrftoken = Cookies.get('csrftoken');
      let url = '';
      if(type=="STOP"){
        setIcon('power');
        setExecutionStatus('stopped');
        url = 'https://backend.grabbereat.com/stopprocess';
      }else{
        setIcon('stop');
        setExecutionStatus('running');
        url = 'https://backend.grabbereat.com/startprocess';
      }
      const response = await axios.post(
        url, 
        {
          username: username,
          type: type
        }, 
        {
          headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
          }
        }
      );
  
      // On success, update the icon and fetch execution status
      setIcon(type === 'START' ? 'stop' : 'power');
      fetchExecutionStatus();  // Use await to make sure the status is updated after the process starts/stops
    } catch (error) {
      setIcon(type === 'START' ? 'stop' : 'power');
      // If an error occurs, still fetch execution status and log the error
      await fetchExecutionStatus();
      console.error('Error in plan data:', error);
    } finally {
      setLoadingStatus(false); // End loading when done
    }
  };
  
  const fetchExecutionStatus = async () => {
    try {
      const response = await axios.get('https://backend.grabbereat.com/check_execution_status?username=' + username);
      const status = response.data.execution_status;
      setExecutionStatus(status);
      setIcon(status === 'running' ? 'stop' : 'power');
    } catch (error) {
      console.error('Error fetching execution status:', error);
    }
  };
  
  useEffect(() => {
    fetchCurrentPlan();
    fetchExecutionStatus();
  }, []);

  const styles = {
    container: {
      padding: '20px',
      maxWidth: '100%',
      backgroundColor: '#121212',
      color: '#fff',
      minHeight: '100vh',
      marginLeft: isHamburgerVisible ? '0px' : '250px',
    },
    header: { marginTop: '50px' },
    iconTransition: {
      transition: 'transform 0.3s ease, opacity 0.3s ease', // Smooth transition for transform and opacity
      width: '240px',
      height: 'auto',
      cursor: 'pointer',
    },
    statusText: {
      marginTop: '10px',
      color: 'lightgreen',
    },
    planInfoContainer: {
      marginBottom: '20px',
      padding: '10px',
      backgroundColor: '#2c2c2c',
      borderRadius: '5px',
      color: 'white',
    },
    modalContent: {
      position: 'absolute',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      bgcolor: 'background.paper',
      border: '2px solid #000',
      boxShadow: 24,
      p: 4,
      width: '300px',
    },
    loading: {
      color: 'lightgray',
    },
  };

  const fetchCurrentPlan = () => {
    const planData = JSON.parse(localStorage.getItem('currentPlan'));
    setCurrentPlan(planData);
    setLoadingPlan(false);
  };

  const handleSaveCredentials = () => {
    // POST JustEat credentials to the backend for validation and saving
    const sendCredentials = { username: username, justeatemail: justEatUsername, justeatpw: justEatPassword };
    const credentials = { username: justEatUsername, password: justEatPassword };
    const csrftoken = Cookies.get('csrftoken');

    axios.post('https://backend.grabbereat.com/save_justeat_credentials', sendCredentials, {
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      if (response.data.success) {
        localStorage.setItem('justEatCredentials', JSON.stringify(credentials)); // Save credentials to localStorage
        setOpenModal(false); // Close modal after saving
        // Proceed with the action after credentials are saved
        handleClick('START');
      } else {
        console.error('Invalid credentials:', response.data.message);
        alert('Invalid JustEat credentials');
      }
    })
    .catch(error => {
      console.error('Error saving JustEat credentials:', error);
      alert('Error saving credentials');
    });
  };

  return (
    <div style={styles.container}>
      <Typography variant="h4" style={styles.header} gutterBottom>
        Dashboard
      </Typography>

      {loadingPlan ? (
        <Typography variant="h6" color="textSecondary">Loading your plan...</Typography>
      ) : currentPlan ? (
        <Box style={styles.planInfoContainer}> 

          {(justEat.username && justEat.password) ? ( 
          <>
          <Typography variant="h6">
            Current Plan: {currentPlan.plan_name}
          </Typography>
          <Typography variant="body1">
            Expiry Date: {new Date(currentPlan.expiry_date).toLocaleDateString()}
          </Typography>
          </>) : (<></>
          )}

          {icon === 'power' ? (
            <PowerSettingsNewIcon
              style={styles.iconTransition}
              onClick={() => handleClick('START')}
              sx={{
                color: loadingStatus ? grey[500] : 'primary.main', // Disabled color when loading
                cursor: loadingStatus ? 'not-allowed' : 'pointer',
                pointerEvents: loadingStatus ? 'none' : 'auto',
              }}
            />
          ) : (
            <StopIcon
              style={styles.iconTransition}
              onClick={() => handleClick('STOP')}
              sx={{
                color: loadingStatus ? grey[500] : 'secondary.main', // Disabled color when loading
                cursor: loadingStatus ? 'not-allowed' : 'pointer',
                pointerEvents: loadingStatus ? 'none' : 'auto',
              }}
            />
          )}
          {loadingStatus ? ( // Show loading spinner when loadingStatus is true
            <Box style={{ textAlign: 'center', marginTop: '10px' }}>
              <CircularProgress color="secondary" />
            </Box>
          ) : (<></>)}

          <Typography variant="h6" style={styles.statusText}>
            {executionStatus === 'running' ? 'Running' : 'Stopped'}
          </Typography>
        </Box>
      ) : (
        <Typography variant="h6" color="textSecondary">No plan found</Typography>
      )}

      <Modal
        open={openModal}
        onClose={() => setOpenModal(false)}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box style={styles.modalContent}>
          <TextField
            label="JustEat Username"
            variant="outlined"
            fullWidth
            value={justEatUsername}
            onChange={(e) => setJustEatUsername(e.target.value)}
            style={{ marginBottom: '10px' }}
          />
          <TextField
            label="JustEat Password"
            variant="outlined"
            type="password"
            fullWidth
            value={justEatPassword}
            onChange={(e) => setJustEatPassword(e.target.value)}
            style={{ marginBottom: '10px' }}
          />
          <Button
            variant="contained"
            color="primary"
            fullWidth
            onClick={handleSaveCredentials}
          >
            Save Credentials
          </Button>
        </Box>
      </Modal>
      
      {/* Other accordions and toggles */}
      <Accordion href="/logs">
        <AccordionSummary
           expandIcon={<ExpandMore />}
          aria-controls="logs-content"
          id="logs-header"
        >
          <FaClipboardList style={{ color: 'white', marginRight: '10px' }} />
          <Link href="/logs" underline="none">
            <Typography>Logs</Typography>
          </Link>
        </AccordionSummary>
      </Accordion>

      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMore />}
          aria-controls="schedule-content"
          id="schedule-header"
        >
          <FaCalendarAlt style={{ color: 'white', marginRight: '10px' }} />
          <Link href="/schedule" underline="none">
            <Typography>Schedule</Typography>
          </Link>
        </AccordionSummary>
      </Accordion>

      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMore />}
          aria-controls="zones-content"
          id="zones-header"
        >
          <FaMapMarkerAlt style={{ color: 'white', marginRight: '10px' }} />
          <Link href="/zones" underline="none">
            <Typography>Zones</Typography>
          </Link>
        </AccordionSummary>
      </Accordion>

      {/* Toggling accordions for "Open Run" and "Overflow" */}
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMore />}
          aria-controls="open-run-content"
          id="open-run-header"
        >
          <Typography>Open Run Toggle</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <FormControlLabel
            control={
              <Switch
                checked={openRun}
                onChange={handleOpenRunToggle}
                name="openRun"
              />
            }
            label={openRun ? 'Yes' : 'No'}
          />
        </AccordionDetails>
      </Accordion>

      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMore />}
          aria-controls="overflows-content"
          id="overflows-header"
        >
          <Typography>Overflows Toggle</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <FormControlLabel
            control={
              <Switch
                checked={overflows}
                onChange={handleOverflowsToggle}
                name="overflows"
              />
            }
            label={overflows ? 'Yes' : 'No'}
          />
        </AccordionDetails>
      </Accordion>
    </div>
  );
};

export default DashboardPage;
