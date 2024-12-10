import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom"; // useParams to capture referral code from URL, useNavigate for redirecting
import axios from "axios"; // For making API requests
import Cookies from "js-cookie"; // For handling CSRF tokens
import { CircularProgress, Box, Typography } from "@mui/material"; // Material UI components

const Referral = () => {
  const [loading, setLoading] = useState(true);
  const [referralResponse, setReferralResponse] = useState(null);
  const [error, setError] = useState(null);
  const [userIp, setUserIp] = useState(null); // State to store user IP address

  const { referralCode } = useParams(); // { referralCode } will capture the part after `/referrals/`
  const navigate = useNavigate(); // For redirecting to the signup page

  // Function to capture user IP address
  const fetchUserIp = async () => {
    try {
      const response = await axios.get("https://api.ipify.org?format=json"); // Get IP address
      setUserIp(response.data.ip);
    } catch (error) {
      console.error("Error fetching IP address:", error);
      setError("Unable to fetch IP address.");
    }
  };

  // Handle the referral code submission to the backend
  const handleSubmit = () => {
    if (!referralCode) {
      setError("No referral code found.");
      setLoading(false);
      return;
    }

    if (!userIp) {
      setError("Unable to fetch user IP address.");
      setLoading(false);
      return;
    }

    const csrftoken = Cookies.get("csrftoken"); // Get CSRF token for security

    // Send the referral code to the backend for processing
    axios
      .post(
        "https://backend.grabbereat.com/submit_referral", // Adjust this URL to match your backend endpoint
        {
          referral_code: referralCode,
          session_key: sessionStorage.getItem("sessionKey") ? sessionStorage.getItem("sessionKey") : "", // Get session key from sessionStorage
          user_ip: userIp, // Pass the user's IP address
        },
        {
          headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
          },
        }
      )
      .then((response) => {
        setReferralResponse(response.data);
        setLoading(false);

        // Check if the referral response status is "success"
        if (response.data.referral_response && response.data.referral_response.status === "success") {
          // Generate a session key if not already generated
          if (!sessionStorage.getItem("sessionKey")) {
            const sessionKey = generateSessionKey();
            sessionStorage.setItem("sessionKey", sessionKey); // Store session key in sessionStorage
          }

          // Redirect to the signup page
          navigate("/signUp/"+referralCode); // Redirecting to the signup page
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        setError("There was an error processing your referral.");
        setLoading(false);
      });
  };

  // Generate a session key (simple random string generator for the session)
  const generateSessionKey = () => {
    return "session-" + Math.random().toString(36).substr(2, 9); // Random session key generator
  };

  useEffect(() => {
    if (referralCode) {
      fetchUserIp(); // Fetch user IP address on component mount
    } else {
      setError("No referral code found in the URL.");
      setLoading(false);
    }
  }, [referralCode]);

  useEffect(() => {
    if (userIp) {
      handleSubmit(); // Trigger referral response handling once IP address is available
    }
  }, [userIp]); // Trigger handleSubmit when IP address is available

  // Show loading spinner while waiting for the response
  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" }}>
        <CircularProgress />
      </Box>
    );
  }

  // Show error if any occurs
  if (error) {
    return (
      <Box sx={{ padding: 3 }}>
        <Typography variant="h6" color="error">{error}</Typography>
      </Box>
    );
  }

  // Show referral response if available
  return (
    <Box sx={{ padding: 3 }}>
      <Typography variant="h4" color="textPrimary">Referral Response</Typography>
      {referralResponse ? (
        <Typography variant="body1" color="textSecondary">
          Thank you for responding to the referral! Here's your response data:
          <pre>{JSON.stringify(referralResponse, null, 2)}</pre>
        </Typography>
      ) : (
        <Typography variant="body1" color="textSecondary">Referral link has been processed.</Typography>
      )}
    </Box>
  );
};

export default Referral;
