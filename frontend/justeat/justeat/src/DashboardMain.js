// src/components/DashboardMain.js
import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';

const DashboardContent = styled.div`
  margin-left: 250px; /* Sidebar width */
  margin-top: 80px; /* Space for topbar */
  padding: 20px;
`;

const StatBox = styled.div`
  background-color: #ecf0f1;
  padding: 20px;
  margin: 10px;
  border-radius: 5px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  display: inline-block;
  width: 30%;
`;

const DashboardMain = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Fetch dashboard data
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/dashboard'); // Replace with your actual API
        setData(response.data);
      } catch (error) {
        console.error('Error fetching dashboard data', error);
      }
    };

    fetchData();
  }, []);

  return (
    <DashboardContent>
      <h2>Welcome to Your Dashboard</h2>
      <div>
        <StatBox>
          <h3>Total Shifts</h3>
          <p>{data ? data.totalShifts : 'Loading...'}</p>
        </StatBox>
        <StatBox>
          <h3>Upcoming Shifts</h3>
          <p>{data ? data.upcomingShifts : 'Loading...'}</p>
        </StatBox>
        <StatBox>
          <h3>Completed Shifts</h3>
          <p>{data ? data.completedShifts : 'Loading...'}</p>
        </StatBox>
      </div>
    </DashboardContent>
  );
};

export default DashboardMain;
