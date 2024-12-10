import React, { useState, useEffect } from 'react';
import { Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TextField, TablePagination, Accordion, AccordionSummary, AccordionDetails } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useSidebar } from './SidebarContext'; // Import the custom hook

// Sample log data (mock data)
let logData = [
];

      

const LogsPage = () => {
  const username = localStorage.getItem('userName');
  const [logs, setLogs] = useState(logData);
  const [page, setPage] = useState(0);
  const [error, setError] = useState('');
  const { isDrawerOpen, isHamburgerVisible } = useSidebar();

  const handleSubmit = () => {
    // Get CSRF token if needed
    const csrftoken = Cookies.get('csrftoken');
    axios.post('https://backend.grabbereat.com/logs', {
      username: username
    }, {
      headers: {
        'X-CSRFToken': csrftoken,  // Include CSRF token in the request headers
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      if (response.data) {
        console.log('Login successful:', response.data);
        // Handle successful login (e.g., redirect or update UI)
        setLogs(response.data.logs);
      }else{
        
      }
    })
    .catch(error => {
      console.error('Error logging in:', error);
      // Handle error (e.g., show error message)
      setError('Invalid log data');
    });
  };

  useEffect(() => {
    handleSubmit();
  }, []);

  const [rowsPerPage, setRowsPerPage] = useState(5);
  const [filter, setFilter] = useState('');

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleFilterChange = (event) => {
    setFilter(event.target.value);
  };

  const filteredLogs = logs.filter(log =>
    log.message.toLowerCase().includes(filter.toLowerCase())
  );


  return (
    <Box sx={{ display: 'flex', padding: '20px', backgroundColor: '#121212', color: 'white' }}>
      <Box sx={{ flex: 1, marginLeft: isHamburgerVisible ? '0px' : '250px', padding: '20px' }}>
        <Typography variant="h4"  color="white" marginTop="50px"  gutterBottom sx={{ color: 'white' }}>Logs</Typography>


        {/* Table for displaying logs */}
        <TableContainer component={Paper} sx={{ backgroundColor: '#1D1D1D' }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell sx={{ color: 'white' }}>Date</TableCell>
                <TableCell sx={{ color: 'white' }}>Time</TableCell>
                <TableCell sx={{ color: 'white' }}>Zone</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredLogs.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((log) => (
                <TableRow key={log.id}>
                  <TableCell sx={{ color: 'white' }}>{log.date}</TableCell>
                  <TableCell sx={{ color: 'white' }}>{log.time}</TableCell>
                  <TableCell sx={{ color: 'white' }}>{log.Zone}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        {/* Pagination */}
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={filteredLogs.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          sx={{
            '& .MuiTablePagination-select': {
              color: 'white',
            },
            '& .MuiTablePagination-toolbar': {
              backgroundColor: '#1D1D1D',
            },
          }}
        />
      </Box>
    </Box>
  );
};

export default LogsPage;
