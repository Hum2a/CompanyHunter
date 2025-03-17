from abc import ABC, abstractmethod

class BaseJobConnector(ABC):
    """Base class for all job API connectors"""
    
    def __init__(self, api_key=None, app_id=None):
        self.api_key = api_key
        self.app_id = app_id
        self.name = self.__class__.__name__
    
    @abstractmethod
    async def search_jobs(self, location, radius, categories=None, job_types=None):
        """
        Search for jobs based on location and filters
        
        Args:
            location (str): Location string (city, address, etc.)
            radius (float): Search radius in km
            categories (list): List of job categories to filter by
            job_types (list): List of job types to filter by
            
        Returns:
            list: List of standardized job objects
        """
        pass
    
    @abstractmethod
    def get_categories(self):
        """
        Get available job categories for this API
        
        Returns:
            list: List of category strings
        """
        pass
    
    @abstractmethod
    def get_job_types(self):
        """
        Get available job types for this API
        
        Returns:
            list: List of job type strings
        """
        pass
    
    def standardize_job(self, job_data):
        """
        Convert API-specific job data to standard format
        
        Args:
            job_data (dict): API-specific job data
            
        Returns:
            dict: Standardized job object
        """
        # This should be implemented by each connector
        # but providing a base implementation for safety
        return {
            "title": "Unknown",
            "company": {
                "display_name": "Unknown"
            },
            "location": {
                "area": []
            },
            "description": "No description available",
            "redirect_url": "",
            "source_api": self.name,
            "latitude": None,
            "longitude": None,
            "category": {
                "label": "Unknown"
            },
            "contract_type": "Unknown",
            "created": None,
            "company_metadata": {
                "address": "N/A",
                "phone": "N/A",
                "website": "N/A",
                "maps_url": "N/A"
            }
        } 