// Layout.js
import React from 'react';
import { Outlet } from 'react-router-dom'; // Outlet is used to render nested routes
import Sidebar from './Sidebar'; // Assuming Sidebar is in the same directory

const Layout = () => {
  return (
    <div style={{ display: 'flex' }}>
      <Sidebar />
      <main style={{ flexGrow: 1, padding: '20px', backgroundColor: '#121212', minHeight: '100vh' }}>
        <Outlet /> {/* This will render the page content based on the route */}
      </main>
    </div>
  );
};

export default Layout;
