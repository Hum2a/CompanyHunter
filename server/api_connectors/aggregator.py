import asyncio
from typing import List, Dict, Any, Optional
import os
import math
import requests

class JobAggregator:
    """Aggregates job results from multiple API connectors."""
    
    def __init__(self):
        self.connectors = []
        
    def add_connector(self, connector):
        """Add a job search connector to the aggregator."""
        self.connectors.append(connector)
    
    def get_categories(self):
        """Get combined list of categories from all connectors."""
        all_categories = set()
        for connector in self.connectors:
            all_categories.update(connector.get_categories())
        return sorted(list(all_categories))
    
    def get_job_types(self):
        """Get combined list of job types from all connectors."""
        all_job_types = set()
        for connector in self.connectors:
            all_job_types.update(connector.get_job_types())
        return sorted(list(all_job_types))
    
    async def search_jobs(self, location, radius, categories=None, job_types=None):
        """Search for jobs across all connectors and return combined results."""
        print(f"[Aggregator] Searching for jobs in {location} within {radius}km")
        
        # Get coordinates for location using Google Maps API
        GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_MAPS_API_KEY}"
        geocode_response = requests.get(geocode_url)
        geocode_data = geocode_response.json()
        
        if geocode_data['status'] != 'OK':
            raise ValueError('Could not geocode location')
        
        # Extract coordinates
        coordinates = geocode_data['results'][0]['geometry']['location']
        lat = coordinates['lat']
        lng = coordinates['lng']
        
        # Get formatted address for the search area
        formatted_address = geocode_data['results'][0].get('formatted_address', '')
        print(f"[Aggregator] Formatted address: {formatted_address}")
        
        # Gather tasks for each connector
        tasks = []
        for connector in self.connectors:
            print(f"[Aggregator] Adding search task for {connector.__class__.__name__}")
            # Handle both async and synchronous connectors
            if hasattr(connector, 'search_jobs') and callable(connector.search_jobs):
                try:
                    task = connector.search_jobs(
                        location=formatted_address,
                        radius=radius,
                        categories=categories,
                        job_types=job_types
                    )
                    # If the connector returns a coroutine, add it as a task
                    if asyncio.iscoroutine(task):
                        tasks.append(task)
                    else:
                        # If it's a synchronous function, wrap it in a completed future
                        future = asyncio.Future()
                        future.set_result(task)
                        tasks.append(future)
                except Exception as e:
                    print(f"[Aggregator] Error creating task for {connector.__class__.__name__}: {str(e)}")
        
        # Wait for all tasks to complete
        results = []
        if tasks:
            try:
                connector_results = await asyncio.gather(*tasks, return_exceptions=True)
                for result in connector_results:
                    if isinstance(result, Exception):
                        print(f"[Aggregator] Connector error: {str(result)}")
                    elif isinstance(result, list):
                        results.extend(result)
            except Exception as e:
                print(f"[Aggregator] Error gathering results: {str(e)}")
        
        # Deduplicate and normalize results
        processed_results = self._process_results(results, lat, lng, radius)
        
        print(f"[Aggregator] Found {len(processed_results)} jobs after processing")
        return processed_results
    
    def _process_results(self, all_jobs, lat, lng, radius):
        """Process all job results by deduplicating and enriching data."""
        # Track jobs by title+company to avoid duplicates
        unique_jobs = {}
        processed_jobs = []
        
        # Company blacklist
        COMPANY_BLACKLIST = []
        
        for job in all_jobs:
            # Skip if company is in blacklist
            company_name = job.get('company', {}).get('display_name', '')
            if company_name in COMPANY_BLACKLIST:
                print(f"[Aggregator] Company {company_name} is blacklisted, skipping")
                continue
            
            # Add unique ID if not present
            if 'id' not in job:
                title = job.get('title', '')
                job['id'] = f"{title}_{company_name}_{len(processed_jobs)}"
            
            # Handle jobs without location data or distance calculation
            job_lat = job.get('latitude')
            job_lng = job.get('longitude')
            
            # If no coordinates or distance, add it with calculated distance
            if not job_lat or not job_lng or 'distance' not in job:
                job_lat = lat
                job_lng = lng
                job['latitude'] = job_lat
                job['longitude'] = job_lng
            
            # Calculate distance if not provided
            if 'distance' not in job:
                distance = self._calculate_distance(lat, lng, job_lat, job_lng)
                job['distance'] = distance
            
            # Skip if outside radius
            if job['distance'] > radius:
                continue
            
            # Check for duplicates (same title and company)
            job_key = f"{job.get('title', '')}__{company_name}"
            
            # If we haven't seen this job before, or this instance has more data, keep it
            if job_key not in unique_jobs or self._has_more_data(job, unique_jobs[job_key]):
                unique_jobs[job_key] = job
        
        # Convert dict to list
        processed_jobs = list(unique_jobs.values())
        
        # Sort by distance
        processed_jobs.sort(key=lambda x: x.get('distance', float('inf')))
        
        return processed_jobs
    
    def _has_more_data(self, new_job, existing_job):
        """Check if new job has more data than existing job."""
        # Check if the new job has more fields with actual values
        new_job_data_count = sum(1 for v in new_job.values() if v is not None and v != '')
        existing_job_data_count = sum(1 for v in existing_job.values() if v is not None and v != '')
        
        return new_job_data_count > existing_job_data_count
    
    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points in kilometers using Haversine formula."""
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        
        return c * r 