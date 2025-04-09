import React from 'react';
import { motion } from 'framer-motion';
import CompanyResults from '../CompanyResults';

const fadeIn = {
  hidden: { opacity: 0, y: 20 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { 
      duration: 0.5,
      ease: "easeOut"
    } 
  }
};

const ResultsSection = ({ results, onSaveCompany }) => {
  return (
    <motion.div 
      className="results-section"
      variants={fadeIn}
      initial="hidden"
      animate="visible"
    >
      <CompanyResults 
        results={results} 
        onSaveCompany={onSaveCompany}
      />
    </motion.div>
  );
};

export default ResultsSection; 