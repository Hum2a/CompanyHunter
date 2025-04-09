import { useState } from 'react';
import { API_URL } from '../config/constants';

export const useJobSearch = () => {
  const [center, setCenter] = useState({ lat: 51.5074, lng: -0.1278 }); // Default to London
  const [radius, setRadius] = useState(10); // Default radius in km
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({ categories: [], jobTypes: [] });

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
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

  return {
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
  };
};