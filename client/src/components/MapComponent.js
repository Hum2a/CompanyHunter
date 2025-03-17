import React, { useEffect, useRef, useState } from 'react';
import { GoogleMap, useJsApiLoader, Marker, Circle } from '@react-google-maps/api';

const containerStyle = {
  width: '100%',
  height: '400px'
};

const MapComponent = ({ center, radius, setCenter, setRadius }) => {
  const mapRef = useRef(null);
  const circleRef = useRef(null);
  const [map, setMap] = useState(null);
  
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY
  });

  const onLoad = React.useCallback(function callback(map) {
    mapRef.current = map;
    setMap(map);
  }, []);

  const onUnmount = React.useCallback(function callback(map) {
    mapRef.current = null;
    setMap(null);
  }, []);

  const onCircleLoad = React.useCallback(circle => {
    circleRef.current = circle;
  }, []);

  // Update radius when the circle is dragged
  const onRadiusChanged = React.useCallback(() => {
    if (circleRef.current) {
      setRadius(circleRef.current.getRadius() / 1000); // Convert meters to kilometers
    }
  }, [setRadius]);

  // Update center when the map is clicked
  const onMapClick = React.useCallback((e) => {
    setCenter({
      lat: e.latLng.lat(),
      lng: e.latLng.lng()
    });
  }, [setCenter]);

  return isLoaded ? (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={10}
      onLoad={onLoad}
      onUnmount={onUnmount}
      onClick={onMapClick}
    >
      <Marker position={center} />
      <Circle
        center={center}
        radius={radius * 1000} // Convert km to meters
        onLoad={onCircleLoad}
        onRadiusChanged={onRadiusChanged}
        options={{
          fillColor: 'rgba(66, 133, 244, 0.2)',
          fillOpacity: 0.35,
          strokeColor: '#4285F4',
          strokeOpacity: 0.8,
          strokeWeight: 2,
          editable: true,
          draggable: false
        }}
      />
    </GoogleMap>
  ) : <div>Loading...</div>;
};

export default MapComponent; 