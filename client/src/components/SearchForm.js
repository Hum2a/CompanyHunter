import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { filterLocations } from '../data/ukLocations';
import "../styles/SearchForm.css";

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
  const [suggestions, setSuggestions] = useState([]);
  const [activeSuggestionIndex, setActiveSuggestionIndex] = useState(-1);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [activeInputIndex, setActiveInputIndex] = useState(-1);

  const handleLocationChange = (index, value) => {
    const newLocations = [...locations];
    newLocations[index] = value;
    setLocations(newLocations);

    // Update suggestions
    if (value.trim()) {
      const filtered = filterLocations(value);
      setSuggestions(filtered);
      setShowSuggestions(true);
      setActiveSuggestionIndex(-1);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  };

  const handleKeyDown = (e, index) => {
    if (!showSuggestions) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setActiveSuggestionIndex(prev => 
          prev < suggestions.length - 1 ? prev + 1 : prev
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setActiveSuggestionIndex(prev => 
          prev > 0 ? prev - 1 : -1
        );
        break;
      case 'Enter':
        e.preventDefault();
        if (activeSuggestionIndex >= 0) {
          handleLocationChange(index, suggestions[activeSuggestionIndex]);
          setShowSuggestions(false);
        }
        break;
      case 'Escape':
        setShowSuggestions(false);
        break;
      default:
        break;
    }
  };

  const handleSuggestionClick = (index, suggestion) => {
    handleLocationChange(index, suggestion);
    setShowSuggestions(false);
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

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (!e.target.closest('.location-input-group')) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, []);

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
              <div className="location-input-wrapper">
                <motion.input
                  type="text"
                  value={location}
                  onChange={(e) => handleLocationChange(index, e.target.value)}
                  onKeyDown={(e) => handleKeyDown(e, index)}
                  onFocus={() => {
                    setActiveInputIndex(index);
                    setIsFocused(true);
                    if (location.trim()) {
                      setShowSuggestions(true);
                    }
                  }}
                  placeholder="Enter location (e.g., London)"
                  className="location-input"
                  disabled={isLoading}
                  variants={inputVariants}
                  initial="blur"
                  whileFocus="focus"
                  animate={isFocused ? "focus" : "blur"}
                />
                {showSuggestions && activeInputIndex === index && suggestions.length > 0 && (
                  <div className="suggestions-dropdown">
                    {suggestions.map((suggestion, i) => (
                      <div
                        key={i}
                        className={`suggestion-item ${i === activeSuggestionIndex ? 'active' : ''}`}
                        onClick={() => handleSuggestionClick(index, suggestion)}
                      >
                        {suggestion}
                      </div>
                    ))}
                  </div>
                )}
              </div>
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