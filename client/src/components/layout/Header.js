import React from 'react';
import { motion } from 'framer-motion';
import Logo from '../Logo';
import AnimatedBackground from '../AnimatedBackground';

const Header = () => {
  return (
    <motion.header 
      className="App-header"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <AnimatedBackground />
      <Logo />
    </motion.header>
  );
};

export default Header; 