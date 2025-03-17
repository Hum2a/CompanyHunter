import asyncio
import hashlib
import json
from .base_connector import BaseJobConnector

class JobAggregator:
    """Aggregates results from multiple job API connectors"""
    
    def __init__(self):
        self.connectors = []
        self.all_categories = []
        self.all_job_types = []
    
    def add_connector(self, connector):
        """Add a job API connector to the aggregator"""
        if not isinstance(connector, BaseJobConnector):
            raise TypeError("Connector must be an instance of BaseJobConnector")
        
        self.connectors.append(connector)
        
        # Update available categories and job types
        self._update_available_options()
        
        return self
    
    def _update_available_options(self):
        """Update the list of available categories and job types across all connectors"""
        # Collect categories from all connectors
        categories = set()
        for connector in self.connectors:
            categories.update(connector.get_categories())
        self.all_categories = sorted(list(categories))
        
        # Collect job types from all connectors
        job_types = set()
        for connector in self.connectors:
            job_types.update(connector.get_job_types())
        self.all_job_types = sorted(list(job_types))
    
    def get_categories(self):
        """Get all available job categories across all connectors"""
        return self.all_categories
    
    def get_job_types(self):
        """Get all available job types across all connectors"""
        return self.all_job_types
    
    async def search_jobs(self, location, radius, categories=None, job_types=None):
        """Search for jobs across all connectors"""
        print(f"[Aggregator] Searching for jobs across {len(self.connectors)} connectors")
        print(f"[Aggregator] Location: {location}, Radius: {radius}km")
        print(f"[Aggregator] Categories: {categories}")
        print(f"[Aggregator] Job Types: {job_types}")
        
        if not self.connectors:
            print("[Aggregator] No connectors available")
            return []
        
        # Create tasks for all connectors
        tasks = []
        for connector in self.connectors:
            # Get connector-specific categories and job types
            connector_categories = connector.get_categories()
            connector_job_types = connector.get_job_types()
            
            # Filter categories and job types to those supported by this connector
            filtered_categories = categories if not categories else [
                c for c in categories if c in connector_categories
            ]
            
            filtered_job_types = job_types if not job_types else [
                t for t in job_types if t in connector_job_types
            ]
            
            # Create a search task
            task = asyncio.create_task(
                connector.search_jobs(
                    location,
                    radius,
                    filtered_categories,
                    filtered_job_types
                )
            )
            tasks.append(task)
        
        # Wait for all searches to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Flatten and deduplicate results
        all_jobs = []
        job_ids = set()
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"[Aggregator] Error from connector {self.connectors[i].name}: {str(result)}")
                continue
                
            for job in result:
                # Generate a unique ID for the job based on title, company and location
                job_key = f"{job.get('title', '')}-{job.get('company', {}).get('display_name', '')}-{'-'.join(job.get('location', {}).get('area', []))}"
                job_id = hashlib.md5(job_key.encode()).hexdigest()
                
                if job_id not in job_ids:
                    job_ids.add(job_id)
                    job['id'] = job_id  # Add ID to job for client-side handling
                    all_jobs.append(job)
        
        print(f"[Aggregator] Found {len(all_jobs)} unique jobs")
        
        # Sort by most recent first
        all_jobs.sort(key=lambda j: j.get('created', ''), reverse=True)
        
        return all_jobs 