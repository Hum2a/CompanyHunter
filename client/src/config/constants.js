// API Configuration
export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Map Configuration
export const DEFAULT_CENTER = { lat: 51.5074, lng: -0.1278 }; // London
export const DEFAULT_RADIUS = 10; // kilometers
export const DEFAULT_ZOOM = 10;
export const MAX_ZOOM = 15;

// Animation Configuration
export const ANIMATION_DURATION = 0.5;
export const ANIMATION_DELAY = 0.3;

// Job Types Colors
export const JOB_TYPE_COLORS = {
  full_time: '#e8f5e9',
  part_time: '#e3f2fd',
  contract: '#fff3e0',
  temporary: '#fce4ec',
  permanent: '#f3e5f5',
  remote: '#e8eaf6',
  default: '#f5f5f5'
};

// API Source Colors
export const API_SOURCE_COLORS = {
  Adzuna: '#e8f5e9',
  Reed: '#e3f2fd',
  Google: '#fce4ec',
  Indeed: '#fff3e0',
  default: '#f5f5f5'
}; 