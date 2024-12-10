import React from 'react';
import { Accordion, AccordionSummary, AccordionDetails, Typography, Box } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'; // To show the expand/collapse icon

// FAQ Data (You can adjust the text here as per the exact FAQ content you want to use)
const faqData = [
  {
    question: 'What is GrabberEat?',
    answer: 'GrabberEat is a platform that allows you to manage and optimize your shift scheduling, making it easier for businesses to organize their workforce.',
  },
  {
    question: 'How does GrabberEat work?',
    answer: 'GrabberEat allows you to create schedules, assign shifts to employees, and track their work hours in a user-friendly dashboard.',
  },
  {
    question: 'Can I customize shift templates?',
    answer: 'Yes, GrabberEat allows you to create custom templates based on your business needs, making it easier to assign shifts based on specific requirements.',
  },
  {
    question: 'Is GrabberEat available on mobile?',
    answer: 'Yes, GrabberEat is available as a mobile app for both iOS and Android devices, making it easy to manage your shifts on the go.',
  },
  {
    question: 'How can I sign up?',
    answer: 'You can sign up by clicking the "Sign Up" button on our homepage and filling in the necessary details. It\'s fast and easy!',
  },
];

function FAQSection() {
  return (
    <Box sx={{ width: '100%', maxWidth: 800, margin: '0 auto' }}>
      <Typography variant="h4" align="center" sx={{ mb: 4 }}>
        Frequently Asked Questions
      </Typography>
      
      {faqData.map((item, index) => (
        <Accordion key={index} sx={{ mb: 2 }}>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls={`panel${index}-content`}
            id={`panel${index}-header`}
          >
            <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
              {item.question}
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography variant="body1" sx={{ color: 'text.secondary' }}>
              {item.answer}
            </Typography>
          </AccordionDetails>
        </Accordion>
      ))}
    </Box>
  );
}

export default FAQSection;
