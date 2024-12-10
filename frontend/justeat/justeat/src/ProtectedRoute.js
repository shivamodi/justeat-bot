import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';


const isAuthenticated = !!localStorage.getItem('isAuthenticated');

const ProtectedRoute = ( isAuthenticated ) => {
  return isAuthenticated ? <Outlet /> : <Navigate to="/signIn" />;
};

export default ProtectedRoute;
