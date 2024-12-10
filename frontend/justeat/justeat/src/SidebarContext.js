// SidebarContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';

// Create Context
const SidebarContext = createContext();

// SidebarProvider component to wrap around the app and provide context
export const SidebarProvider = ({ children }) => {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false); // Drawer open state
  const [isHamburgerVisible, setHamburgerVisible] = useState(false); // Hamburger visibility

  // Function to handle screen resizing and control hamburger visibility
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth <= 768) {
        setHamburgerVisible(true); // Show hamburger icon on mobile
        setIsDrawerOpen(false); // Ensure drawer is closed on mobile
      } else {
        setHamburgerVisible(false); // Hide hamburger on desktop
        setIsDrawerOpen(true); // Always open drawer on desktop
      }
    };

    handleResize(); // Initial check

    // Add resize event listener
    window.addEventListener('resize', handleResize);

    return () => window.removeEventListener('resize', handleResize); // Cleanup
  }, []);

  // Function to toggle the drawer (open/close on mobile)
  const toggleDrawer = () => {
    setIsDrawerOpen((prevState) => !prevState);
  };

  return (
    <SidebarContext.Provider value={{ isDrawerOpen, toggleDrawer, isHamburgerVisible }}>
      {children}
    </SidebarContext.Provider>
  );
};

// Custom hook to use sidebar context
export const useSidebar = () => {
  return useContext(SidebarContext);
};
