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
          const sourceApi = job.source_api || 'Unknown';
          
          // Log the job data to see what we're working with
          console.log(`Job ${index + 1}:`, job);
          console.log(`Job ${index + 1} metadata:`, metadata);
          
          return (
            <div key={job.id || index} className="company-card">
              <div className="card-header">
                <h3>{companyName}</h3>
                <span className="source-api">{sourceApi}</span>
              </div>
              <div className="job-title">{job.title || 'N/A'}</div>
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
                {job.location && job.location.area && job.location.area.length > 0 ? (
                  <p><strong>Location:</strong> {job.location.area.join(', ')}</p>
                ) : null}
                
                {/* Show category if available */}
                {job.category && job.category.label ? (
                  <p><strong>Category:</strong> {job.category.label}</p>
                ) : null}
                
                {/* Show salary if available */}
                {job.salary_min && job.salary_max ? (
                  <p><strong>Salary Range:</strong> {job.currency || '£'}{Math.round(job.salary_min).toLocaleString()} - {job.currency || '£'}{Math.round(job.salary_max).toLocaleString()}</p>
                ) : job.salary_min ? (
                  <p><strong>Salary:</strong> {job.currency || '£'}{Math.round(job.salary_min).toLocaleString()}</p>
                ) : null}
                
                {/* Show contract type if available */}
                {job.contract_type ? (
                  <p><strong>Contract Type:</strong> {job.contract_type.replace('_', ' ')}</p>
                ) : null}
                
                {/* Created date */}
                {job.created ? (
                  <p><strong>Posted:</strong> {new Date(job.created).toLocaleDateString()}</p>
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