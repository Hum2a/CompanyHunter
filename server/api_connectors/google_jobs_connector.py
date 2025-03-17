import os
import aiohttp
import json
from datetime import datetime
from .base_connector import BaseJobConnector

class GoogleJobsConnector(BaseJobConnector):
    """Connector for the Google Jobs API (Cloud Talent Solution)"""
    
    # Common job categories in Google Jobs
    JOB_CATEGORIES = [
        "IT Jobs",
        "Engineering Jobs",
        "Healthcare & Nursing Jobs",
        "Finance Jobs",
        "Marketing Jobs",
        "Sales Jobs",
        "Administrative Jobs",
        "Education Jobs",
        "Manufacturing Jobs",
        "Retail Jobs",
        "Customer Service Jobs",
        "Legal Jobs"
    ]

    # Job types
    JOB_TYPES = [
        "FULL_TIME",
        "PART_TIME",
        "CONTRACTOR",
        "TEMPORARY",
        "INTERN",
        "VOLUNTEER",
        "PER_DIEM",
        "OTHER"
    ]
    
    # Mapping from Google job types to our standard types
    JOB_TYPE_MAPPING = {
        "FULL_TIME": "full_time",
        "PART_TIME": "part_time",
        "CONTRACTOR": "contract",
        "TEMPORARY": "contract",
        "INTERN": "internship",
        "VOLUNTEER": "other",
        "PER_DIEM": "other",
        "OTHER": "other"
    }
    
    def __init__(self, client_id=None, client_secret=None, project_id=None):
        super().__init__()
        self.client_id = client_id or os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('GOOGLE_CLIENT_SECRET')
        self.project_id = project_id or os.getenv('GOOGLE_PROJECT_ID')
        self.name = "Google Jobs"
        
        # Google Cloud Talent Solution API endpoint for HTTP requests
        self.base_url = f"https://jobs.googleapis.com/v4/projects/{self.project_id}/tenants/default/jobs:search"
    
    def get_categories(self):
        """Get available job categories for Google Jobs"""
        return self.JOB_CATEGORIES
    
    def get_job_types(self):
        """Get available job types for Google Jobs"""
        return self.JOB_TYPES
    
    async def search_jobs(self, location, radius, categories=None, job_types=None):
        """Search for jobs on Google Jobs API"""
        print(f"[GoogleJobs] Searching for jobs in {location} within {radius}km")
        
        if not self.client_id or not self.client_secret or not self.project_id:
            print("[GoogleJobs] Credentials or project ID not configured")
            return []
            
        # In a real implementation, we'd make the API request here
        # But for now, let's return dummy data to avoid dependency issues
        print(f"[GoogleJobs] Returning dummy data for {location}")
        
        # Create a dummy job result
        dummy_job = self._create_dummy_job(location)
        
        return [dummy_job]
    
    def _create_dummy_job(self, location):
        """Create a dummy job for demonstration purposes"""
        return {
            "id": f"google-jobs-{datetime.now().timestamp()}",
            "title": "Software Engineer",
            "company": {
                "display_name": "Google"
            },
            "location": {
                "area": [location]
            },
            "description": "This is a dummy job created by the Google Jobs connector for demonstration purposes.",
            "redirect_url": "https://careers.google.com/",
            "source_api": self.name,
            "latitude": None,
            "longitude": None,
            "category": {
                "label": "IT Jobs"
            },
            "contract_type": "full_time",
            "created": datetime.now().isoformat(),
            "salary_min": 80000,
            "salary_max": 150000,
            "currency": "USD",
            "company_metadata": {
                "address": f"Google Office, {location}",
                "phone": "N/A",
                "website": "https://google.com",
                "maps_url": "N/A"
            }
        }