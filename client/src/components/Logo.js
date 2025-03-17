import React from 'react';
import { motion } from 'framer-motion';

const Logo = () => {
  return (
    <motion.div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '10px',
      }}
    >
      <motion.div
        style={{
          width: '40px',
          height: '40px',
          borderRadius: '8px',
          background: 'white',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          color: '#5e72e4',
          fontWeight: 'bold',
          fontSize: '20px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        }}
        initial={{ rotate: -180, scale: 0 }}
        animate={{ rotate: 0, scale: 1 }}
        transition={{
          type: 'spring',
          stiffness: 200,
          damping: 15,
        }}
      >
        CH
      </motion.div>
      <motion.span
        style={{
          fontSize: '24px',
          fontWeight: 'bold',
          color: 'white',
        }}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.3, duration: 0.5 }}
      >
        CompanyHunter
      </motion.span>
    </motion.div>
  );
};

export default Logo; 