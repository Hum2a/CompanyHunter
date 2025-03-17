import React, { useState } from 'react';

const SearchForm = ({ onSearch, center, radius, setRadius, isLoading }) => {
  const [location, setLocation] = useState('');
  const [searchRadius, setSearchRadius] = useState(radius);

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
    <div className="search-form">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="location">Location (or click on map):</label>
          <input
            type="text"
            id="location"
            placeholder="City, Address, or Postal Code"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="form-control"
            disabled={isLoading}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="radius">Radius (km): {searchRadius} km</label>
          <input
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
          />
        </div>
        
        <button type="submit" className="btn btn-primary" disabled={isLoading}>
          {isLoading ? 'Searching...' : 'Search Jobs'}
        </button>
      </form>
    </div>
  );
};

export default SearchForm; 