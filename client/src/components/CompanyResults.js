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

const CompanyResults = ({ results, onSaveCompany }) => {
  if (!results || results.length === 0) {
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

  return (
    <div className="company-results">
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        Jobs Found ({results.length})
      </motion.h2>
      
      <motion.div 
        className="results-list"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {results.map((job, index) => {
          const company = job.company || {};
          const companyName = company.display_name || 'N/A';
          const metadata = job.company_metadata || {};
          const sourceApi = job.source_api || 'Unknown';
          
          return (
            <motion.div 
              key={job.id || index} 
              className="company-card"
              variants={cardVariants}
              whileHover="hover"
              layoutId={`job-${index}`}
            >
              <div className="card-header">
                <h3>{companyName}</h3>
                <motion.span 
                  className="source-api"
                  whileHover={{ scale: 1.1 }}
                >
                  {sourceApi}
                </motion.span>
              </div>
              
              <motion.div 
                className="job-title"
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                {job.title || 'N/A'}
              </motion.div>
              
              <div className="company-details">
                <p><strong>Distance:</strong> {job.distance ? `${job.distance.toFixed(2)} km` : 'N/A'}</p>
                
                {metadata.address && metadata.address !== 'N/A' ? (
                  <p><strong>Address:</strong> {metadata.address}</p>
                ) : null}
                
                {metadata.phone && metadata.phone !== 'N/A' ? (
                  <p><strong>Phone:</strong> {metadata.phone}</p>
                ) : null}
                
                {metadata.website && metadata.website !== 'N/A' ? (
                  <p><strong>Website:</strong> <a href={metadata.website} target="_blank" rel="noopener noreferrer">{metadata.website}</a></p>
                ) : job.redirect_url ? (
                  <p><strong>Job Listing:</strong> <a href={job.redirect_url} target="_blank" rel="noopener noreferrer">View Job Posting</a></p>
                ) : null}
                
                {metadata.maps_url && metadata.maps_url !== 'N/A' ? (
                  <p><strong>Maps:</strong> <a href={metadata.maps_url} target="_blank" rel="noopener noreferrer">View on Google Maps</a></p>
                ) : null}
                
                {/* Show original job location if available */}
                {job.location && job.location.area && Array.isArray(job.location.area) && job.location.area.length > 0 ? (
                  <p><strong>Location:</strong> {job.location.area.join(', ')}</p>
                ) : null}
                
                {/* Display salary information if available */}
                {(job.salary_min || job.salary_max) ? (
                  <p>
                    <strong>Salary:</strong> {' '}
                    {job.salary_min ? `${job.currency || '£'}${job.salary_min.toLocaleString()}` : ''}
                    {job.salary_min && job.salary_max ? ' - ' : ''}
                    {job.salary_max ? `${job.currency || '£'}${job.salary_max.toLocaleString()}` : ''}
                  </p>
                ) : null}
                
                {/* Show contract type if available */}
                {job.contract_type ? (
                  <p><strong>Type:</strong> {job.contract_type}</p>
                ) : null}
                
                {/* Show category if available */}
                {job.category && job.category.label ? (
                  <p><strong>Category:</strong> {job.category.label}</p>
                ) : null}
              </div>
              
              {job.description ? (
                <div className="job-description">
                  <h4>Description</h4>
                  <div dangerouslySetInnerHTML={{ __html: job.description }} />
                </div>
              ) : null}
              
              <motion.button
                className="btn btn-success"
                onClick={() => onSaveCompany(job)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Save Job
              </motion.button>
            </motion.div>
          );
        })}
      </motion.div>
    </div>
  );
};

export default CompanyResults; 