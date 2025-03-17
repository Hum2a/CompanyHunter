import os
import aiohttp
import json
import base64
from datetime import datetime
from .base_connector import BaseJobConnector

class ReedConnector(BaseJobConnector):
    """Connector for the Reed.co.uk Jobs API"""
    
    # Common job categories in Reed
    JOB_CATEGORIES = [
        "Accountancy Jobs",
        "Admin, Secretarial & PA Jobs",
        "Banking Jobs",
        "Charity & Voluntary Jobs",
        "Customer Services Jobs",
        "Education Jobs",
        "Engineering Jobs",
        "Estate Agency Jobs",
        "Financial Services Jobs",
        "General Insurance Jobs",
        "Graduate Training & Internships",
        "Health & Medicine Jobs",
        "Hospitality & Catering Jobs",
        "Human Resources Jobs",
        "IT & Telecoms Jobs",
        "Legal Jobs",
        "Leisure & Tourism Jobs",
        "Manufacturing Jobs",
        "Marketing & PR Jobs",
        "Media, Digital & Creative Jobs",
        "Motoring & Automotive Jobs",
        "Public Sector Jobs",
        "Purchasing Jobs",
        "Recruitment Consultancy Jobs",
        "Retail Jobs",
        "Sales Jobs",
        "Scientific Jobs",
        "Security & Safety Jobs",
        "Social Care Jobs",
        "Transport & Logistics Jobs"
    ]

    # Job types
    JOB_TYPES = [
        "permanent",
        "temp",
        "contract",
        "part_time",
        "full_time"
    ]
    
    # Mapping from Reed job types to our standard types
    JOB_TYPE_MAPPING = {
        "permanent": "permanent",
        "temp": "contract",
        "contract": "contract",
        "part_time": "part_time",
        "full_time": "full_time",
        "apprenticeship": "apprenticeship",
        "graduate": "graduate",
        "internship": "internship"
    }
    
    def __init__(self, api_key=None):
        super().__init__(api_key)
        self.api_key = api_key or os.getenv('REED_API_KEY')
        self.base_url = "https://www.reed.co.uk/api/1.0/search"
    
    def get_categories(self):
        """Get available job categories for Reed"""
        return self.JOB_CATEGORIES
    
    def get_job_types(self):
        """Get available job types for Reed"""
        return self.JOB_TYPES
    
    async def search_jobs(self, location, radius, categories=None, job_types=None):
        """Search for jobs on Reed.co.uk"""
        print(f"[Reed] Searching for jobs in {location} within {radius}km")
        
        # Reed API parameters
        params = {
            'locationName': location,
            'distanceFromLocation': radius,
            'resultsToTake': 100
        }
        
        # Add category filters
        if categories and len(categories) > 0:
            # Reed allows only one category at a time, so we'll use the first one
            first_category = categories[0]
            # Remove "Jobs" suffix if present for better matching
            if first_category.endswith(" Jobs"):
                first_category = first_category[:-5]
            params['keywords'] = first_category
        
        # Add job type filters
        if job_types and len(job_types) > 0:
            # Map our job types to Reed job types
            reed_job_types = []
            for job_type in job_types:
                if job_type in self.JOB_TYPE_MAPPING.values():
                    # Find the Reed job type that maps to our job type
                    for reed_type, our_type in self.JOB_TYPE_MAPPING.items():
                        if our_type == job_type and reed_type in self.JOB_TYPES:
                            reed_job_types.append(reed_type)
            
            if reed_job_types:
                # Reed API only supports one job type at a time
                params['fullTime'] = 'true' if 'full_time' in reed_job_types else None
                params['partTime'] = 'true' if 'part_time' in reed_job_types else None
                params['contractType'] = 'permanent' if 'permanent' in reed_job_types else (
                    'contract' if 'contract' in reed_job_types else None
                )
        
        print(f"[Reed] API params: {json.dumps(params)}")
        
        # Reed API uses Basic Authentication with API key as username
        auth_header = f"Basic {base64.b64encode(f'{self.api_key}:'.encode()).decode()}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.base_url, 
                    params=params,
                    headers={"Authorization": auth_header}
                ) as response:
                    if response.status != 200:
                        print(f"[Reed] API error: {response.status}")
                        return []
                    
                    data = await response.json()
                    results = data.get('results', [])
                    
                    print(f"[Reed] Found {len(results)} jobs")
                    
                    # Convert to standard format
                    return [self.standardize_job(job) for job in results]
        except Exception as e:
            print(f"[Reed] Error searching jobs: {str(e)}")
            return []
    
    def standardize_job(self, job_data):
        """Convert Reed job data to standard format"""
        # Map Reed fields to our standard format
        
        # Parse date
        date_posted = None
        if 'datePosted' in job_data:
            try:
                # Reed dates are in format "/Date(1616544000000)/"
                timestamp_str = job_data['datePosted'].strip('/Date()')
                timestamp = int(timestamp_str.split('+')[0]) / 1000  # Convert to seconds
                date_posted = datetime.fromtimestamp(timestamp).isoformat()
            except:
                pass
        
        # Determine job category
        category = "Unknown"
        if 'jobDescription' in job_data and job_data['jobDescription']:
            # Extract from job title or description
            job_title = job_data.get('jobTitle', '')
            for cat in self.JOB_CATEGORIES:
                cat_name = cat.replace(' Jobs', '')
                if cat_name.lower() in job_title.lower() or cat_name.lower() in job_data['jobDescription'].lower():
                    category = cat
                    break
        
        # Map contract type
        contract_type = "Unknown"
        if 'contractType' in job_data:
            reed_contract = job_data['contractType'].lower()
            if reed_contract in self.JOB_TYPE_MAPPING:
                contract_type = self.JOB_TYPE_MAPPING[reed_contract]
        
        # Build company display name
        company_name = job_data.get('employerName', 'Unknown')
        
        return {
            "title": job_data.get('jobTitle', 'Unknown Position'),
            "company": {
                "display_name": company_name
            },
            "location": {
                "area": [job_data.get('locationName', 'Unknown'), job_data.get('townName', '')]
            },
            "description": job_data.get('jobDescription', 'No description available'),
            "redirect_url": job_data.get('jobUrl', ''),
            "source_api": self.name,
            "latitude": job_data.get('latitude'),
            "longitude": job_data.get('longitude'),
            "category": {
                "label": category
            },
            "contract_type": contract_type,
            "created": date_posted,
            "salary_min": job_data.get('minimumSalary'),
            "salary_max": job_data.get('maximumSalary'),
            "currency": "GBP",
            "company_metadata": {
                "address": f"{job_data.get('locationName', '')}, {job_data.get('townName', '')}",
                "phone": "N/A",
                "website": "N/A",
                "maps_url": "N/A"
            }
        } 