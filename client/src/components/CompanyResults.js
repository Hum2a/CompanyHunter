import React from 'react';
import { motion } from 'framer-motion';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const cardVariants = {
  hidden: { y: 50, opacity: 0 },
  visible: { 
    y: 0, 
    opacity: 1,
    transition: {
      type: 'spring',
      damping: 12,
      stiffness: 100
    }
  },
  hover: {
    y: -10,
    boxShadow: "0 15px 30px rgba(0, 0, 0, 0.2)"
  }
};

const CompanyResults = ({ results, onSaveCompany, searchAreas }) => {
  const formatSalary = (min, max) => {
    if (!min && !max) return 'Salary not specified';
    if (!max) return `From £${min.toLocaleString()}`;
    if (!min) return `Up to £${max.toLocaleString()}`;
    return `£${min.toLocaleString()} - £${max.toLocaleString()}`;
  };

  const getCompanyName = (company) => {
    if (!company) return 'Unknown Company';
    if (typeof company === 'string') return company;
    return company.display_name || 'Unknown Company';
  };

  const getLocationText = (location) => {
    console.log('Getting location text for:', location);
    if (!location) {
      console.log('Location is null/undefined');
      return 'Location not specified';
    }
    if (typeof location === 'string') {
      console.log('Location is string:', location);
      return location;
    }
    if (typeof location === 'object') {
      console.log('Location is object:', location);
      if (location.display_name) {
        console.log('Using display_name:', location.display_name);
        return location.display_name;
      }
      if (location.name) {
        console.log('Using name:', location.name);
        return location.name;
      }
      if (location.address) {
        console.log('Using address:', location.address);
        return location.address;
      }
      if (location.area && Array.isArray(location.area) && location.area.length > 0) {
        console.log('Using area array:', location.area[0]);
        return location.area[0];
      }
    }
    console.log('No valid location format found, returning Unknown Location');
    return 'Unknown Location';
  };

  const getLocationBadge = (searchLocation) => {
    console.log('Getting location badge for:', searchLocation);
    if (!searchLocation) {
      console.log('No search location provided');
      return null;
    }
    const locationText = getLocationText(searchLocation);
    console.log('Location badge text:', locationText);
    return (
      <span className="location-badge">
        {locationText}
      </span>
    );
  };

  const formatSearchAreas = (areas) => {
    console.log('Formatting search areas:', areas);
    if (!areas || !Array.isArray(areas)) {
      console.log('Invalid areas format, returning default');
      return '1 location';
    }
    const formattedAreas = areas.map(area => {
      console.log('Processing area:', area);
      return getLocationText(area);
    });
    console.log('Formatted areas:', formattedAreas);
    return `${formattedAreas.length} location${formattedAreas.length > 1 ? 's' : ''}`;
  };

  if (!results || results.length === 0) {
    console.log('No results to display');
    return (
      <motion.div 
        className="empty-results"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        No jobs found. Try adjusting your search criteria or expanding your radius.
      </motion.div>
    );
  }

  console.log('Rendering results:', results);
  console.log('Search areas:', searchAreas);

  return (
    <div className="results-container">
      <h2 className="results-title">
        Found {results.length} jobs in {formatSearchAreas(searchAreas)}
      </h2>
      
      <div className="results-grid">
        {results.map((job, index) => (
          <motion.div
            key={index}
            className="job-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <div className="job-header">
              <h3 className="job-title">{job.title || 'Untitled Position'}</h3>
              <div className="job-meta">
                <span className="company-name">{getCompanyName(job.company)}</span>
                <span className="job-type">{job.job_type || 'Full-time'}</span>
                {job.searchLocation && getLocationBadge(job.searchLocation)}
              </div>
            </div>
            
            <div className="job-details">
              <p className="job-description">{job.description || 'No description available'}</p>
              <div className="job-info">
                <span className="salary">{formatSalary(job.salary_min, job.salary_max)}</span>
                <span className="location">{getLocationText(job.location)}</span>
              </div>
            </div>
            
            <div className="job-actions">
              <a
                href={job.url}
                target="_blank"
                rel="noopener noreferrer"
                className="apply-button"
              >
                Apply Now
              </a>
              <button
                onClick={() => onSaveCompany(job)}
                className="save-button"
              >
                Save Job
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default CompanyResults; 