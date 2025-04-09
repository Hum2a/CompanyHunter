import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import SearchSection from '../components/sections/SearchSection';
import ResultsSection from '../components/sections/ResultsSection';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import { useJobSearch } from '../hooks/useJobSearch';
import { API_URL } from '../config/constants';
import MapComponent from '../components/MapComponent';
import SearchForm from '../components/SearchForm';
import FilterOptions from '../components/FilterOptions';
import CompanyResults from '../components/CompanyResults';
import AnimatedBackground from '../components/AnimatedBackground';
import Logo from '../components/Logo';

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

const HomePage = () => {
  const [center, setCenter] = useState({ lat: 51.5074, lng: -0.1278 }); // Default to London
  const [radius, setRadius] = useState(10);
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({ categories: [], jobTypes: [] });
  const [searchAreas, setSearchAreas] = useState([]);

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  const handleSearch = async (searchParams) => {
    try {
      setError(null);
      setLoading(true);
      
      console.log('Search params received:', searchParams);
      console.log('Locations before formatting:', searchParams.locations);
      
      // Store the search areas for display
      const formattedSearchAreas = searchParams.locations.map(location => {
        console.log('Processing location:', location);
        const formattedLocation = typeof location === 'string' ? location : location.display_name || 'Unknown Location';
        console.log('Formatted location:', formattedLocation);
        return formattedLocation;
      });
      
      console.log('Formatted search areas:', formattedSearchAreas);
      setSearchAreas(formattedSearchAreas);
      
      // Combine results from all locations
      const allResults = [];
      
      for (const location of searchParams.locations) {
        console.log('Processing location for API call:', location);
        const locationText = typeof location === 'string' ? location : location.display_name || 'Unknown Location';
        console.log('Location text for API:', locationText);
        
        const params = new URLSearchParams({
          location: locationText,
          radius: searchParams.radius
        });
        
        filters.categories.forEach(category => {
          params.append('category', category);
        });
        
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
        console.log(`Found ${data.total} jobs for ${locationText}`);
        console.log('First job data:', data.results?.[0]);
        
        if (data.error) {
          throw new Error(data.error);
        }
        
        // Add location information to each job
        const jobsWithLocation = (data.results || []).map(job => {
          const jobWithLocation = {
            ...job,
            searchLocation: locationText,
            coordinates: job.coordinates || {
              latitude: job.latitude,
              longitude: job.longitude
            }
          };
          console.log('Job with location:', jobWithLocation);
          return jobWithLocation;
        });
        
        allResults.push(...jobsWithLocation);
      }
      
      console.log('All results before setting state:', allResults);
      
      // Update the center to the first location's coordinates if available
      if (allResults.length > 0 && allResults[0].coordinates) {
        setCenter({
          lat: allResults[0].coordinates.latitude,
          lng: allResults[0].coordinates.longitude
        });
      }
      
      setResults(allResults);
      
    } catch (err) {
      console.error("Search error:", err);
      setError(err.message || "An error occurred while searching for jobs.");
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const { handleSaveCompany } = useJobSearch();

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
              searchAreas={searchAreas}
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
                searchAreas={searchAreas}
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
};

export default HomePage; 