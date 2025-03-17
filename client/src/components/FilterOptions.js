import React, { useState, useEffect } from 'react';

const FilterOptions = ({ onFilterChange, apiUrl }) => {
  const [categories, setCategories] = useState([]);
  const [jobTypes, setJobTypes] = useState([]);
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [selectedJobTypes, setSelectedJobTypes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expanded, setExpanded] = useState(false);

  // Fetch available categories and job types from the API
  useEffect(() => {
    const fetchFilters = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${apiUrl}/api/categories`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch filter options');
        }
        
        const data = await response.json();
        setCategories(data.categories || []);
        setJobTypes(data.job_types || []);
        setError(null);
      } catch (err) {
        console.error('Error fetching filters:', err);
        setError('Could not load filter options');
        // Set some defaults in case the API fails
        setCategories([
          "IT Jobs", 
          "Engineering Jobs", 
          "Healthcare & Nursing Jobs",
          "Teaching Jobs",
          "Accounting & Finance Jobs"
        ]);
        setJobTypes([
          "full_time",
          "part_time",
          "contract",
          "permanent"
        ]);
      } finally {
        setLoading(false);
      }
    };
    
    fetchFilters();
  }, [apiUrl]);
  
  // Handle category selection
  const handleCategoryChange = (category) => {
    let newCategories;
    if (selectedCategories.includes(category)) {
      newCategories = selectedCategories.filter(c => c !== category);
    } else {
      newCategories = [...selectedCategories, category];
    }
    setSelectedCategories(newCategories);
    triggerFilterChange(newCategories, selectedJobTypes);
  };
  
  // Handle job type selection
  const handleJobTypeChange = (jobType) => {
    let newJobTypes;
    if (selectedJobTypes.includes(jobType)) {
      newJobTypes = selectedJobTypes.filter(t => t !== jobType);
    } else {
      newJobTypes = [...selectedJobTypes, jobType];
    }
    setSelectedJobTypes(newJobTypes);
    triggerFilterChange(selectedCategories, newJobTypes);
  };
  
  // Reset all filters
  const handleReset = () => {
    setSelectedCategories([]);
    setSelectedJobTypes([]);
    triggerFilterChange([], []);
  };
  
  // Notify parent component about filter changes
  const triggerFilterChange = (categories, jobTypes) => {
    onFilterChange({
      categories,
      jobTypes
    });
  };
  
  // Format job type for display
  const formatJobType = (type) => {
    return type.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };
  
  return (
    <div className="filter-options">
      <div className="filter-header" onClick={() => setExpanded(!expanded)}>
        <h3>
          <span>Filter Options</span>
          <span className={`toggle-icon ${expanded ? 'expanded' : ''}`}>
            {expanded ? '▼' : '►'}
          </span>
        </h3>
        {!expanded && selectedCategories.length + selectedJobTypes.length > 0 && (
          <div className="active-filters-summary">
            {selectedCategories.length + selectedJobTypes.length} filters active
          </div>
        )}
      </div>
      
      {expanded && (
        <div className="filter-body">
          {loading ? (
            <div className="loading-filters">Loading filter options...</div>
          ) : error ? (
            <div className="filter-error">{error}</div>
          ) : (
            <>
              <div className="filter-section">
                <h4>Job Categories</h4>
                <div className="filter-options-grid">
                  {categories.map(category => (
                    <div className="filter-option" key={category}>
                      <label>
                        <input
                          type="checkbox"
                          checked={selectedCategories.includes(category)}
                          onChange={() => handleCategoryChange(category)}
                        />
                        {category}
                      </label>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="filter-section">
                <h4>Job Types</h4>
                <div className="filter-options-grid">
                  {jobTypes.map(jobType => (
                    <div className="filter-option" key={jobType}>
                      <label>
                        <input
                          type="checkbox"
                          checked={selectedJobTypes.includes(jobType)}
                          onChange={() => handleJobTypeChange(jobType)}
                        />
                        {formatJobType(jobType)}
                      </label>
                    </div>
                  ))}
                </div>
              </div>
              
              {(selectedCategories.length > 0 || selectedJobTypes.length > 0) && (
                <button className="btn btn-secondary" onClick={handleReset}>
                  Reset Filters
                </button>
              )}
            </>
          )}
        </div>
      )}
      
      {expanded && selectedCategories.length + selectedJobTypes.length > 0 && (
        <div className="active-filters">
          <h4>Active Filters:</h4>
          <div className="filter-tags">
            {selectedCategories.map(category => (
              <span key={category} className="filter-tag">
                {category}
                <button onClick={() => handleCategoryChange(category)}>×</button>
              </span>
            ))}
            {selectedJobTypes.map(jobType => (
              <span key={jobType} className="filter-tag">
                {formatJobType(jobType)}
                <button onClick={() => handleJobTypeChange(jobType)}>×</button>
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default FilterOptions; 