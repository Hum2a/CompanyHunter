import os
import aiohttp
import json
from .base_connector import BaseJobConnector

class AdzunaConnector(BaseJobConnector):
    """Connector for the Adzuna Jobs API"""
    
    # Common job categories in Adzuna
    JOB_CATEGORIES = [
        "IT Jobs", 
        "Engineering Jobs", 
        "Healthcare & Nursing Jobs",
        "Teaching Jobs",
        "Trade & Construction Jobs",
        "Accounting & Finance Jobs",
        "Sales Jobs",
        "Admin Jobs",
        "Scientific & QA Jobs",
        "Hospitality & Catering Jobs",
        "Retail Jobs",
        "Social work Jobs",
        "PR, Advertising & Marketing Jobs",
        "Logistics & Warehouse Jobs",
        "Creative & Design Jobs",
        "Manufacturing Jobs",
        "Legal Jobs",
        "Customer Services Jobs",
        "HR & Recruitment Jobs",
        "Property Jobs"
    ]

    # Common job types
    JOB_TYPES = [
        "full_time",
        "part_time",
        "contract",
        "permanent",
        "apprenticeship",
        "internship",
        "graduate"
    ]
    
    def __init__(self, app_id=None, api_key=None):
        super().__init__(api_key, app_id)
        self.app_id = app_id or os.getenv('ADZUNA_APP_ID')
        self.api_key = api_key or os.getenv('ADZUNA_API_KEY')
        self.base_url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"
    
    def get_categories(self):
        """Get available job categories for Adzuna"""
        return self.JOB_CATEGORIES
    
    def get_job_types(self):
        """Get available job types for Adzuna"""
        return self.JOB_TYPES
    
    async def search_jobs(self, location, radius, categories=None, job_types=None):
        """Search for jobs on Adzuna"""
        print(f"[Adzuna] Searching for jobs in {location} within {radius}km")
        
        # Use a larger search radius for Adzuna to ensure we get results
        api_radius = int(radius * 2)  # Double the radius for the API search
        if api_radius < 10:
            api_radius = 10  # Minimum 10km for API search
            
        # Build Adzuna API URL with filters
        params = {
            'app_id': self.app_id,
            'app_key': self.api_key,
            'results_per_page': 100,
            'where': location,
            'distance': api_radius
        }
        
        # Add category filters
        if categories:
            category_param = " OR ".join([f"category:{category}" for category in categories])
            params['what'] = category_param
        
        # Add job type filters
        if job_types:
            for job_type in job_types:
                params['contract_type'] = job_type
        
        print(f"[Adzuna] API params: {json.dumps(params)}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status != 200:
                        print(f"[Adzuna] API error: {response.status}")
                        return []
                    
                    data = await response.json()
                    
                    print(f"[Adzuna] Found {data.get('count', 0)} jobs")
                    
                    # If no results, try a more generic search
                    if not data.get('results'):
                        print("[Adzuna] No results, trying generic search")
                        # Remove location-specific params
                        generic_params = params.copy()
                        if 'where' in generic_params:
                            del generic_params['where']
                        if 'distance' in generic_params:
                            del generic_params['distance']
                        
                        async with session.get(self.base_url, params=generic_params) as generic_response:
                            if generic_response.status != 200:
                                return []
                            
                            data = await generic_response.json()
                            print(f"[Adzuna] Generic search found {data.get('count', 0)} jobs")
                    
                    # Convert to standard format
                    return [self.standardize_job(job) for job in data.get('results', [])]
        except Exception as e:
            print(f"[Adzuna] Error searching jobs: {str(e)}")
            return []
    
    def standardize_job(self, job_data):
        """Convert Adzuna job data to standard format"""
        # Adzuna data is already close to our standard format
        # Just add the source API info
        job_data['source_api'] = self.name
        
        # Ensure company_metadata exists
        if 'company_metadata' not in job_data:
            job_location = job_data.get('location', {})
            area = job_location.get('area', [])
            area_str = ", ".join(area) if area else "N/A"
            
            job_data['company_metadata'] = {
                'address': area_str,
                'phone': 'N/A',
                'website': job_data.get('redirect_url', 'N/A'),
                'maps_url': 'N/A'
            }
        
        return job_data 