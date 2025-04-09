import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import SearchSection from '../components/sections/SearchSection';
import ResultsSection from '../components/sections/ResultsSection';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import { useJobSearch } from '../hooks/useJobSearch';
import { API_URL } from '../config/constants';

const HomePage = () => {
  const {
    center,
    setCenter,
    radius,
    setRadius,
    results,
    error,
    loading,
    filters,
    handleFilterChange,
    handleSearch,
    handleSaveCompany
  } = useJobSearch();

  return (
    <div className="App">
      <Header />
      
      <div className="container">
        <SearchSection 
          center={center}
          setCenter={setCenter}
          radius={radius}
          setRadius={setRadius}
          filters={filters}
          onFilterChange={handleFilterChange}
          onSearch={handleSearch}
          loading={loading}
          apiUrl={API_URL}
        />
        
        <AnimatePresence mode="wait">
          {error && (
            <motion.div 
              className="error-message"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              key="error"
            >
              <p>{error}</p>
            </motion.div>
          )}
          
          {loading && (
            <motion.div 
              className="loading-indicator"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              key="loading"
            >
              <div className="spinner"></div>
              <p className="loading-text">Searching for jobs...</p>
            </motion.div>
          )}
          
          {!loading && !error && (
            <ResultsSection 
              results={results}
              onSaveCompany={handleSaveCompany}
            />
          )}
        </AnimatePresence>
      </div>
      
      <Footer />
    </div>
  );
};

export default HomePage; 