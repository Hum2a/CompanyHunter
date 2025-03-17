import React, { useState } from 'react';
import './App.css';
import { motion, AnimatePresence } from 'framer-motion';
import MapComponent from './components/MapComponent';
import SearchForm from './components/SearchForm';
import CompanyResults from './components/CompanyResults';
import FilterOptions from './components/FilterOptions';
import AnimatedBackground from './components/AnimatedBackground';
import Logo from './components/Logo';

// Get API URL from environment variables or use default
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Animation variants
const fadeIn = {
  hidden: { opacity: 0, y: 20 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { 
      duration: 0.5,
      ease: "easeOut"
    } 
  },
  exit: { 
    opacity: 0,
    y: -20,
    transition: { 
      duration: 0.3,
      ease: "easeIn"
    } 
  }
};

function App() {
  const [center, setCenter] = useState({ lat: 51.5074, lng: -0.1278 }); // Default to London
  const [radius, setRadius] = useState(10); // Default radius in km
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({ categories: [], jobTypes: [] });

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    // If we already have results, don't trigger a new search automatically
    // The user will need to click search again to apply the filters
  };

  const handleSearch = async (searchParams) => {
    try {
      setError(null);
      setLoading(true);
      
      // Build URL parameters including filters
      const params = new URLSearchParams({
        location: searchParams.location,
        radius: searchParams.radius
      });
      
      // Add category filters
      filters.categories.forEach(category => {
        params.append('category', category);
      });
      
      // Add job type filters
      filters.jobTypes.forEach(jobType => {
        params.append('job_type', jobType);
      });
      
      const searchUrl = `${API_URL}/api/jobs?${params.toString()}`;
      console.log(`Searching for jobs at: ${searchUrl}`);
      
      const response = await fetch(searchUrl);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error(`Error response: ${errorText}`);
        throw new Error(`Server error: ${response.status} ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log(`Found ${data.total} jobs`);
      
      // Check if we received an error from the API
      if (data.error) {
        throw new Error(data.error);
      }
      
      // Update the center if we found coordinates
      if (data.coordinates) {
        setCenter({
          lat: data.coordinates.latitude,
          lng: data.coordinates.longitude
        });
      }
      
      setResults(data.results || []);
      
    } catch (err) {
      console.error("Search error:", err);
      setError(err.message || "An error occurred while searching for jobs.");
      setResults([]);
    } finally {
      setLoading(false);
    }
  };
  
  const handleSaveCompany = async (company) => {
    try {
      const response = await fetch(`${API_URL}/api/save`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(company),
      });
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      
      const data = await response.json();
      alert('Company saved successfully!');
      return data;
    } catch (error) {
      console.error('Error saving company:', error);
      alert(`Error saving company: ${error.message}`);
    }
  };

  return (
    <div className="App">
      <motion.header 
        className="App-header"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <AnimatedBackground />
        <Logo />
      </motion.header>
      
      <div className="container">
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
              markers={results}
            />
          </div>
          
          <div className="search-controls">
            <SearchForm 
              onSearch={handleSearch}
              center={center}
              radius={radius}
              setRadius={setRadius}
              isLoading={loading}
            />
            
            <FilterOptions 
              onFilterChange={handleFilterChange}
              apiUrl={API_URL}
              currentFilters={filters}
            />
          </div>
        </motion.div>
        
        <AnimatePresence mode="wait">
          {error && (
            <motion.div 
              className="error-message"
              variants={fadeIn}
              initial="hidden"
              animate="visible"
              exit="exit"
              key="error"
            >
              <p>{error}</p>
            </motion.div>
          )}
          
          {loading && (
            <motion.div 
              className="loading-indicator"
              variants={fadeIn}
              initial="hidden"
              animate="visible"
              exit="exit"
              key="loading"
            >
              <div className="spinner"></div>
              <p className="loading-text">Searching for jobs...</p>
            </motion.div>
          )}
          
          {!loading && !error && (
            <motion.div 
              className="results-section"
              variants={fadeIn}
              initial="hidden"
              animate="visible"
              exit="exit"
              key="results"
            >
              <CompanyResults 
                results={results} 
                onSaveCompany={handleSaveCompany}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
      
      <motion.footer 
        className="App-footer"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8, duration: 0.5 }}
      >
        <p>&copy; {new Date().getFullYear()} CompanyHunter - Find your dream job</p>
      </motion.footer>
    </div>
  );
}

export default App;
