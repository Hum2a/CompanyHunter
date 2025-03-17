import React from 'react';

const CompanyResults = ({ results, onSaveCompany }) => {
  if (!results || results.length === 0) {
    return <div className="empty-results">No companies found. Try adjusting your search criteria.</div>;
  }

  return (
    <div className="company-results">
      <h2>Companies with Jobs ({results.length})</h2>
      <div className="results-list">
        {results.map((job, index) => {
          const company = job.company || {};
          const companyName = company.display_name || 'N/A';
          const metadata = job.company_metadata || {};
          
          return (
            <div key={index} className="company-card">
              <h3>{companyName}</h3>
              <div className="job-title">{job.title || 'N/A'}</div>
              <div className="company-details">
                <p><strong>Distance:</strong> {job.distance ? `${job.distance.toFixed(2)} km` : 'N/A'}</p>
                <p><strong>Address:</strong> {metadata.address || 'N/A'}</p>
                <p><strong>Phone:</strong> {metadata.phone || 'N/A'}</p>
                {metadata.website && metadata.website !== 'N/A' ? (
                  <p><strong>Website:</strong> <a href={metadata.website} target="_blank" rel="noopener noreferrer">{metadata.website}</a></p>
                ) : (
                  <p><strong>Website:</strong> N/A</p>
                )}
                {metadata.maps_url && metadata.maps_url !== 'N/A' ? (
                  <p><strong>Maps:</strong> <a href={metadata.maps_url} target="_blank" rel="noopener noreferrer">View on Google Maps</a></p>
                ) : null}
              </div>
              
              <div className="job-description">
                <h4>Job Description</h4>
                <div dangerouslySetInnerHTML={{ __html: job.description || 'No description available' }}></div>
              </div>
              
              <button
                className="btn btn-success"
                onClick={() => onSaveCompany(job)}
              >
                Save Company
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default CompanyResults; 