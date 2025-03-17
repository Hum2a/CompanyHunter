import React, { useState } from 'react';
import './App.css';
import MapComponent from './components/MapComponent';
import SearchForm from './components/SearchForm';
import CompanyResults from './components/CompanyResults';
import FilterOptions from './components/FilterOptions';

// Get API URL from environment variables or use default
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

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
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to fetch jobs');
      }
      
      const data = await response.json();
      console.log(`Received ${data.total} results`);
      
      setResults(data.results || []);
      
      if (data.results.length === 0) {
        setError('No companies found in this area. Try expanding your search radius or try a different location.');
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      setError(error.message);
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
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(company)
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to save company');
      }
      
      alert('Company saved successfully!');
    } catch (error) {
      console.error('Error saving company:', error);
      alert('Failed to save company: ' + error.message);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Company Hunter</h1>
        <p>Find companies with job vacancies in your area</p>
      </header>
      
      <main className="container">
        <div className="search-section">
          <div className="map-container">
            <MapComponent
              center={center}
              radius={radius}
              setCenter={setCenter}
              setRadius={setRadius}
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
            />
          </div>
        </div>
        
        {loading && <div className="loading-indicator">Searching for companies...</div>}
        {error && <div className="error-message">{error}</div>}
        
        <div className="results-section">
          <CompanyResults
            results={results}
            onSaveCompany={handleSaveCompany}
          />
        </div>
      </main>
      
      <footer className="App-footer">
        <p>&copy; {new Date().getFullYear()} Company Hunter</p>
      </footer>
    </div>
  );
}

export default App;
