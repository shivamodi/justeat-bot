import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import SignIn from './SignIn'; // Import your SignIn component
import SignUp from './SignUp'; // Import your SignUp component
import Homepage from './Homepage'; // (Optional) If you have a home page or dashboard
import DashboardPage from './DashboardPage';
import ProtectedRoute from './ProtectedRoute';
import LogsPage from './LogsPage';
import SchedulePage from './SchedulePage';
import Layout from './Layout';
import { SidebarProvider } from './SidebarContext'; // Import the SidebarContext provider
import ZonesPage from './ZonesPage';
import SupportPage from './SupportPage';
import ResetPassword from './ResetPassword';
import Account from './Account';
import MembershipPlans from './MembershipPlans';
import SuccessPage from './SuccessPage';
import CancelPage from './CancelPage';
import LogoutPage from './LogoutPage';
import ReferralPage from './ReferralPage';
import Referral from './Referral';
import BillingInfoPage from './BillingInfoPage'

function App() {
  const isAuthenticated = !!localStorage.getItem('isAuthenticated');
  return (
    <SidebarProvider>

    <Router>
      <Routes>
        {/* Default route (e.g. home page) */}
        <Route path="/" element={<Homepage />} />

        {/* Define the route for the referral page */}
        <Route path="/referrals/:referralCode" element={<Referral />} />

        
        {/* Define the route for the referral page */}
        <Route path="/signUp/:referralCode" element={<SignUp />} />

        <Route path="/" element={<Layout />}>
        {/* Default route (e.g. home page) */}
        <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />} >
          <Route  path="/dash" element={<DashboardPage />} />
        </Route>
        
        <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />} >
          <Route  path="/logs" element={<LogsPage />} />
        </Route>

        <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />} >
          <Route  path="/schedule" element={<SchedulePage />} />
        </Route>
        <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />} >
          <Route  path="/zones" element={<ZonesPage />} />
        </Route>
        <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />} >
          <Route  path="/support" element={<SupportPage />} />
        </Route>
        <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />} >
          <Route  path="/account" element={<Account />} />
        </Route>
        <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />} >
          <Route  path="/membership" element={<MembershipPlans />} />
        </Route>        
        <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />} >
          <Route  path="/success" element={<SuccessPage />} />
        </Route>
        <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />} >
          <Route  path="/cancel" element={<CancelPage />} />
        </Route>
        <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />} >
          <Route  path="/referral" element={<ReferralPage />} />
        </Route>
        <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} />} >
          <Route  path="/billing-info" element={<BillingInfoPage />} />
        </Route>
        </Route>
        {/* Sign-In Route */}
        <Route path="/signIn" element={<SignIn />} />
        
        {/* Sign-Up Route */}
        <Route path="/signUp" element={<SignUp />} />
        {/* Sign-Up Route */}
        <Route path="/logout" element={<LogoutPage />} />
        
        {/* Define the reset password route */}
        <Route path="/reset-password/:uid/:token" element={<ResetPassword />} />
        {/* Other routes */}

      </Routes>
    </Router>
    </SidebarProvider>

  );
}

export default App;
