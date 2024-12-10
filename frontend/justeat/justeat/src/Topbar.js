// src/components/Topbar.js
import React from 'react';
import styled from 'styled-components';

const TopbarContainer = styled.div`
  height: 60px;
  background-color: #34495e;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  position: fixed;
  width: 100%;
  top: 0;
  left: 0;
`;

const UserProfile = styled.div`
  display: flex;
  align-items: center;
`;

const UserName = styled.span`
  margin-left: 10px;
  font-size: 18px;
`;

const NotificationIcon = styled.div`
  margin-left: 20px;
  cursor: pointer;
`;

const Topbar = () => {
  return (
    <TopbarContainer>
      <div>GrabberEat Dashboard</div>
      <UserProfile>
        <img
          src="https://via.placeholder.com/30"
          alt="user"
          style={{ borderRadius: '50%' }}
        />
        <UserName>John Doe</UserName>
      </UserProfile>
      <NotificationIcon>🔔</NotificationIcon>
    </TopbarContainer>
  );
};

export default Topbar;
