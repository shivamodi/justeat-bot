import React from 'react';
import { FaTachometerAlt, FaHeadset, FaUsersCog, FaUserCircle, FaBars, FaShareAlt, FaSignOutAlt } from 'react-icons/fa'; // Import the new icon
import { Link, useNavigate } from 'react-router-dom';
import { useSidebar } from './SidebarContext'; // Import the custom hook

const Sidebar = () => {
  const { isDrawerOpen, toggleDrawer, isHamburgerVisible } = useSidebar();
  const navigate = useNavigate();

  const handleMenuItemClick = () => {
    // Close the sidebar when a menu item is clicked
    toggleDrawer();
  };

  const handleLogout = () => {
    // Implement your logout logic here, e.g., clear user data from localStorage
    localStorage.removeItem('userName');
    localStorage.removeItem('isAuthenticated');
    // Redirect to the login page
    navigate('/logout');
  };

  const styles = {
    header: {
      width: '100%',
      height: '60px',
      backgroundColor: '#1e1f25',  // Same as sidebar background
      color: 'white',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '0 20px',
      position: 'fixed',
      top: '0',
      left: '0',
      zIndex: 20,
    },
    logodiv: {
      marginRight: 'auto',
      marginLeft: 'auto',
    },
    logo: {
      maxWidth: '50px',
    },
    hamburgerIcon: {
      display: isHamburgerVisible ? 'block' : 'none',
      fontSize: '30px',
      color: 'white',
      cursor: 'pointer',
      position: 'absolute',
      top: '50%',
      right: '60px',
      transform: 'translateY(-50%)',
      zIndex: 21,
    },
    container: {
      height: '100vh',
      width: isDrawerOpen ? '240px' : '0',
      backgroundColor: '#1e1f25',  // Matching sidebar background
      color: '#fff',
      position: 'fixed',
      top: '60px',  // To account for the header
      left: '0',
      display: 'flex',
      flexDirection: 'column',
      boxShadow: '2px 0px 8px rgba(0,0,0,0.5)',
      transition: 'transform 0.3s ease',
      transform: isDrawerOpen ? 'translateX(0)' : 'translateX(-100%)',
      zIndex: 15,
      alignItems: 'center',
      justifyContent: 'top',
    },
    menuItem: {
      display: 'flex',
      marginLeft: '50px',
      padding: '20px 20px',
      borderRadius: '8px',
      cursor: 'pointer',
      marginBottom: '10px',
      transition: 'all 0.3s ease',
      color: 'white',
      textDecoration: 'none',
      width: '100%',
      display: isHamburgerVisible && !isDrawerOpen ? 'none' : 'flex',
      '&:hover': {
        backgroundColor: '#333',  // Hover effect for background
      },
    },
    icon: {
      fontSize: '30px',
      marginRight: 15,
      color: 'white',
    },
    menuText: {
      fontSize: '22px',
      fontWeight: '500',
      color: 'white',
    },
    '@media (max-width: 768px)': {
      container: {
        width: isDrawerOpen ? '100%' : '0',  // Full width on mobile
        transition: 'width 0.3s ease',
        left: '0',
      },
      icon: {
        fontSize: '40px',
        marginRight: 20,
      },
      menuText: {
        fontSize: '20px',
      },
      logo: {
        display: 'block',
      },
    },
  };

  return (
    <>
      {/* Global Header with Logo and Hamburger Icon */}
      <div style={styles.header}>
        <div style={styles.logodiv}><img style={styles.logo} src="/static/media/logo.png" alt="Logo" /></div>
        <FaBars style={styles.hamburgerIcon} onClick={toggleDrawer} />
      </div>

      {/* Sidebar Drawer */}
      <div style={styles.container}>
        {/* Sidebar Menu Items */}
        <Link to="/dash" style={styles.menuItem} onClick={handleMenuItemClick}>
          <FaTachometerAlt style={styles.icon} />
          <span style={styles.menuText}>Dashboard</span>
        </Link>

        <Link to="/support" style={styles.menuItem} onClick={handleMenuItemClick}>
          <FaHeadset style={styles.icon} />
          <span style={styles.menuText}>Support</span>
        </Link>

        <Link to="/membership" style={styles.menuItem} onClick={handleMenuItemClick}>
          <FaUsersCog style={styles.icon} />
          <span style={styles.menuText}>Membership</span>
        </Link>

        <Link to="/account" style={styles.menuItem} onClick={handleMenuItemClick}>
          <FaUserCircle style={styles.icon} />
          <span style={styles.menuText}>Account</span>
        </Link>

        <Link to="/referral" style={styles.menuItem} onClick={handleMenuItemClick}>
          <FaShareAlt style={styles.icon} />
          <span style={styles.menuText}>Referral</span>
        </Link>

        <div onClick={handleLogout} style={styles.menuItem}>
          <FaSignOutAlt style={styles.icon} />
          <span style={styles.menuText}>Logout</span>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
