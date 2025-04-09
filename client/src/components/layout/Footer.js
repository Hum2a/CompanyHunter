import React from 'react';
import { motion } from 'framer-motion';

const Footer = () => {
  return (
    <motion.footer 
      className="App-footer"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.8, duration: 0.5 }}
    >
      <p>&copy; {new Date().getFullYear()} CompanyHunter - Find your dream job</p>
    </motion.footer>
  );
};

export default Footer; 