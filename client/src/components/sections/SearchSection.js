import React from 'react';
import { motion } from 'framer-motion';
import MapComponent from '../MapComponent';
import SearchForm from '../SearchForm';
import FilterOptions from '../FilterOptions';

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

const SearchSection = ({ 
  center, 
  setCenter, 
  radius, 
  setRadius, 
  filters,
  onFilterChange,
  onSearch,
  loading,
  apiUrl,
  markers = []
}) => {
  return (
    <motion.div 
      variants={fadeIn}
      initial="hidden"
      animate="visible"
      className="search-section"
    >
      <div className="map-container">
        <MapComponent 
          center={center} 
          setCenter={setCenter} 
          radius={radius}
          markers={markers}
        />
      </div>
      
      <div className="search-controls">
        <SearchForm 
          onSearch={onSearch}
          center={center}
          radius={radius}
          setRadius={setRadius}
          isLoading={loading}
        />
        
        <FilterOptions 
          onFilterChange={onFilterChange}
          apiUrl={apiUrl}
          currentFilters={filters}
        />
      </div>
    </motion.div>
  );
};

export default SearchSection;
