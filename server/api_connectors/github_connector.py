import os
import aiohttp
import json
from .base_connector import BaseJobConnector

class GitHubJobsConnector(BaseJobConnector):
    """Connector for the GitHub Jobs API"""
    
    # Common job categories in GitHub Jobs (all are tech-related)
    JOB_CATEGORIES = [
        "IT Jobs",
        "Engineering Jobs",
        "Software Development Jobs", 
        "Web Development Jobs",
        "Mobile Development Jobs",
        "DevOps Jobs",
        "Data Science Jobs"
    ]

    # Job types
    JOB_TYPES = [
        "full_time"  # GitHub Jobs only supports full-time
    ]
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://jobs.github.com/positions.json"
    
    def get_categories(self):
        """Get available job categories for GitHub Jobs"""
        return self.JOB_CATEGORIES
    
    def get_job_types(self):
        """Get available job types for GitHub Jobs"""
        return self.JOB_TYPES
    
    async def search_jobs(self, location, radius, categories=None, job_types=None):
        """Search for jobs on GitHub Jobs"""
        print(f"[GitHub] Searching for jobs in {location}")
        
        # GitHub Jobs parameters - note it doesn't support radius
        params = {
            'location': location
        }
        
        # GitHub Jobs only supports description search for categories
        if categories and len(categories) > 0:
            # Use first category for search
            first_category = categories[0]
            # Remove "Jobs" suffix if present
            if first_category.endswith(" Jobs"):
                first_category = first_category[:-5]
            params['description'] = first_category
        
        # GitHub Jobs only supports full-time flag
        if job_types and "full_time" in job_types:
            params['full_time'] = 'true'
        
        print(f"[GitHub] API params: {json.dumps(params)}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status != 200:
                        print(f"[GitHub] API error: {response.status}")
                        return []
                    
                    results = await response.json()
                    
                    print(f"[GitHub] Found {len(results)} jobs")
                    
                    # Convert to standard format
                    return [self.standardize_job(job) for job in results]
        except Exception as e:
            print(f"[GitHub] Error searching jobs: {str(e)}")
            return []
    
    def standardize_job(self, job_data):
        """Convert GitHub Jobs data to standard format"""
        # Determine job category based on title and description
        category = "IT Jobs"  # Default for GitHub Jobs
        job_title = job_data.get('title', '').lower()
        job_description = job_data.get('description', '').lower()
        
        # Try to determine a more specific category
        if any(keyword in job_title or keyword in job_description for keyword in ['web', 'frontend', 'front-end', 'backend', 'back-end', 'full-stack', 'html', 'css', 'javascript']):
            category = "Web Development Jobs"
        elif any(keyword in job_title or keyword in job_description for keyword in ['mobile', 'android', 'ios', 'swift', 'kotlin', 'react native', 'flutter']):
            category = "Mobile Development Jobs"
        elif any(keyword in job_title or keyword in job_description for keyword in ['devops', 'aws', 'cloud', 'kubernetes', 'docker', 'ci/cd']):
            category = "DevOps Jobs"
        elif any(keyword in job_title or keyword in job_description for keyword in ['data', 'machine learning', 'ai', 'artificial intelligence', 'ml', 'data science']):
            category = "Data Science Jobs"
        
        # Parse location into city/country
        location_parts = job_data.get('location', '').split(',')
        city = location_parts[0].strip() if location_parts else 'Unknown'
        country = location_parts[-1].strip() if len(location_parts) > 1 else ''
        
        return {
            "title": job_data.get('title', 'Unknown Position'),
            "company": {
                "display_name": job_data.get('company', 'Unknown')
            },
            "location": {
                "area": [city, country]
            },
            "description": job_data.get('description', 'No description available'),
            "redirect_url": job_data.get('url', ''),
            "source_api": self.name,
            "latitude": None,  # GitHub Jobs doesn't provide coordinates
            "longitude": None,
            "category": {
                "label": category
            },
            "contract_type": "full_time",  # GitHub Jobs only lists full-time positions
            "created": job_data.get('created_at'),
            "company_metadata": {
                "address": job_data.get('location', 'N/A'),
                "phone": "N/A",
                "website": job_data.get('company_url', 'N/A'),
                "maps_url": "N/A"
            }
        } 