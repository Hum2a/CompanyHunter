import React, { useEffect, useRef, useState } from 'react';
import { GoogleMap, Marker, Circle, InfoWindow, useJsApiLoader } from '@react-google-maps/api';

const MapComponent = ({ center, setCenter, radius, markers, searchAreas }) => {
  const mapRef = useRef(null);
  const [selectedJob, setSelectedJob] = useState(null);
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY
  });

  useEffect(() => {
    if (mapRef.current && markers.length > 0) {
      const bounds = new window.google.maps.LatLngBounds();
      markers.forEach(marker => {
        if (marker.coordinates) {
          bounds.extend({
            lat: marker.coordinates.latitude,
            lng: marker.coordinates.longitude
          });
        }
      });
      mapRef.current.fitBounds(bounds);
    }
  }, [markers]);

  const onMapLoad = (map) => {
    mapRef.current = map;
  };

  const getMarkerColor = (jobType) => {
    const colors = {
      'full-time': '#4285F4',
      'part-time': '#34A853',
      'contract': '#FBBC05',
      'remote': '#EA4335',
      'default': '#4285F4'
    };
    return colors[jobType?.toLowerCase()] || colors.default;
  };

  const formatSalary = (salary) => {
    if (!salary) return 'Salary not specified';
    if (typeof salary === 'string') return salary;
    if (salary.min && salary.max) {
      return `£${salary.min.toLocaleString()} - £${salary.max.toLocaleString()}`;
    }
    return `£${salary.toLocaleString()}`;
  };

  return isLoaded ? (
    <GoogleMap
      mapContainerStyle={{
        width: '100%',
        height: '100%',
        borderRadius: '8px'
      }}
      center={center}
      zoom={10}
      onLoad={onMapLoad}
      options={{
        zoomControl: true,
        streetViewControl: false,
        mapTypeControl: false,
        fullscreenControl: false
      }}
    >
      {/* Center marker */}
      <Marker
        position={center}
        icon={{
          path: window.google.maps.SymbolPath.CIRCLE,
          scale: 7,
          fillColor: '#4285F4',
          fillOpacity: 1,
          strokeColor: '#FFFFFF',
          strokeWeight: 2
        }}
      />

      {/* Search radius circle */}
      <Circle
        center={center}
        radius={radius * 1000} // Convert km to meters
        options={{
          fillColor: '#4285F4',
          fillOpacity: 0.1,
          strokeColor: '#4285F4',
          strokeOpacity: 0.8,
          strokeWeight: 2
        }}
      />

      {/* Job markers */}
      {markers.map((job, index) => {
        if (!job.coordinates) return null;
        
        return (
          <React.Fragment key={index}>
            <Marker
              position={{
                lat: job.coordinates.latitude,
                lng: job.coordinates.longitude
              }}
              icon={{
                path: window.google.maps.SymbolPath.CIRCLE,
                scale: 6,
                fillColor: getMarkerColor(job.job_type),
                fillOpacity: 1,
                strokeColor: '#FFFFFF',
                strokeWeight: 2
              }}
              title={`${job.title} at ${job.company}`}
              onClick={() => setSelectedJob(job)}
            />
            {selectedJob === job && (
              <InfoWindow
                position={{
                  lat: job.coordinates.latitude,
                  lng: job.coordinates.longitude
                }}
                onCloseClick={() => setSelectedJob(null)}
              >
                <div style={{ padding: '8px' }}>
                  <h3 style={{ margin: '0 0 8px 0', fontSize: '14px' }}>{job.title}</h3>
                  <p style={{ margin: '0 0 4px 0', fontSize: '12px' }}>{job.company}</p>
                  <p style={{ margin: '0 0 4px 0', fontSize: '12px' }}>{formatSalary(job.salary)}</p>
                  <p style={{ margin: '0', fontSize: '12px' }}>{job.job_type}</p>
                </div>
              </InfoWindow>
            )}
          </React.Fragment>
        );
      })}

      {/* Search area markers */}
      {searchAreas.map((area, index) => (
        <Marker
          key={`area-${index}`}
          position={area.coordinates || center}
          icon={{
            path: window.google.maps.SymbolPath.CIRCLE,
            scale: 8,
            fillColor: '#34A853',
            fillOpacity: 0.5,
            strokeColor: '#FFFFFF',
            strokeWeight: 2
          }}
          title={`Search Area: ${area}`}
        />
      ))}
    </GoogleMap>
  ) : null;
};

export default MapComponent; 