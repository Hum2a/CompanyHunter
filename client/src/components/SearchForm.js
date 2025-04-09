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
  const [locations, setLocations] = useState(['']);
  const [radiusValue, setRadiusValue] = useState(radius);
  const [isFocused, setIsFocused] = useState(false);

  const handleLocationChange = (index, value) => {
    const newLocations = [...locations];
    newLocations[index] = value;
    setLocations(newLocations);
  };

  const addLocation = () => {
    setLocations([...locations, '']);
  };

  const removeLocation = (index) => {
    const newLocations = locations.filter((_, i) => i !== index);
    setLocations(newLocations);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const validLocations = locations.filter(loc => loc.trim() !== '');
    if (validLocations.length === 0) return;
    
    onSearch({
      locations: validLocations,
      radius: radiusValue
    });
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
      
      <motion.form 
        onSubmit={handleSubmit}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.4 }}
      >
        <div className="locations-container">
          {locations.map((location, index) => (
            <div key={index} className="location-input-group">
              <motion.input
                type="text"
                value={location}
                onChange={(e) => handleLocationChange(index, e.target.value)}
                placeholder="Enter location (e.g., London, UK)"
                className="location-input"
                disabled={isLoading}
                variants={inputVariants}
                initial="blur"
                whileFocus="focus"
                animate={isFocused ? "focus" : "blur"}
                onFocus={() => setIsFocused(true)}
                onBlur={() => setIsFocused(false)}
              />
              {locations.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeLocation(index)}
                  className="remove-location-btn"
                >
                  ×
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            onClick={addLocation}
            className="add-location-btn"
          >
            + Add Another Location
          </button>
        </div>
        
        <motion.div 
          className="form-group"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          <label htmlFor="radius">Search Radius: {radiusValue} km</label>
          <motion.input
            type="range"
            id="radius"
            min="1"
            max="50"
            value={radiusValue}
            onChange={(e) => {
              const value = parseInt(e.target.value);
              setRadiusValue(value);
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
          disabled={isLoading || locations.every(loc => loc.trim() === '')}
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
      </motion.form>
    </motion.div>
  );
};

export default SearchForm; 