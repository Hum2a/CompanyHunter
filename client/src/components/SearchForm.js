import React, { useState } from 'react';
import { motion } from 'framer-motion';

const inputVariants = {
  focus: { 
    scale: 1.02,
    boxShadow: "0 0 0 3px rgba(94, 114, 228, 0.3)" 
  },
  blur: { 
    scale: 1,
    boxShadow: "0 2px 5px rgba(0, 0, 0, 0.02)" 
  }
};

const buttonVariants = {
  hover: { 
    scale: 1.05,
    boxShadow: "0 6px 20px rgba(94, 114, 228, 0.6)"
  },
  tap: { 
    scale: 0.95
  }
};

const SearchForm = ({ onSearch, center, radius, setRadius, isLoading }) => {
  const [location, setLocation] = useState('');
  const [searchRadius, setSearchRadius] = useState(radius);
  const [isFocused, setIsFocused] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      await onSearch({
        location: location || `${center.lat},${center.lng}`,
        radius: searchRadius
      });
    } catch (error) {
      console.error('Error searching:', error);
    }
  };

  return (
    <motion.div 
      className="search-form"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      <motion.h3
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        Search Jobs
      </motion.h3>
      
      <form onSubmit={handleSubmit}>
        <motion.div 
          className="form-group"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <label htmlFor="location">Location (or click on map):</label>
          <motion.input
            type="text"
            id="location"
            placeholder="City, Address, or Postal Code"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="form-control"
            disabled={isLoading}
            variants={inputVariants}
            initial="blur"
            whileFocus="focus"
            animate={isFocused ? "focus" : "blur"}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
          />
        </motion.div>
        
        <motion.div 
          className="form-group"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          <label htmlFor="radius">Search Radius: {searchRadius} km</label>
          <motion.input
            type="range"
            id="radius"
            min="1"
            max="50"
            value={searchRadius}
            onChange={(e) => {
              const value = parseInt(e.target.value);
              setSearchRadius(value);
              setRadius(value);
            }}
            className="form-control"
            disabled={isLoading}
            whileTap={{ scale: 1.05 }}
          />
        </motion.div>
        
        <motion.button 
          type="submit" 
          className="btn btn-primary" 
          disabled={isLoading}
          variants={buttonVariants}
          whileHover="hover"
          whileTap="tap"
          transition={{ type: "spring", stiffness: 400, damping: 10 }}
        >
          {isLoading ? (
            <span>
              <svg 
                className="spinner-icon" 
                width="20" 
                height="20" 
                viewBox="0 0 24 24"
              >
                <motion.path
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10"
                  animate={{ rotate: 360 }}
                  transition={{ 
                    repeat: Infinity, 
                    duration: 1,
                    ease: "linear"
                  }}
                />
              </svg>
              Searching...
            </span>
          ) : (
            'Search Jobs'
          )}
        </motion.button>
        
        <motion.p 
          className="search-help-text"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.7 }}
        >
          Use the filters below to narrow down your results
        </motion.p>
      </form>
    </motion.div>
  );
};

export default SearchForm; 