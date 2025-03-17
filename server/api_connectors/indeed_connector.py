import os
import aiohttp
import json
from datetime import datetime
from .base_connector import BaseJobConnector

class IndeedConnector(BaseJobConnector):
    """Connector for the Indeed Jobs API"""
    
    # Common job categories in Indeed
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
        "fulltime",
        "parttime",
        "contract",
        "temporary",
        "internship",
        "remote"
    ]
    
    # Mapping from Indeed job types to our standard types
    JOB_TYPE_MAPPING = {
        "fulltime": "full_time",
        "parttime": "part_time",
        "contract": "contract",
        "temporary": "contract",
        "internship": "internship",
        "remote": "remote"
    }
    
    def __init__(self, publisher_id=None):
        super().__init__(publisher_id)
        self.publisher_id = publisher_id or os.getenv('INDEED_PUBLISHER_ID')
        self.name = "Indeed"
        self.base_url = "https://api.indeed.com/ads/apisearch"
    
    def get_categories(self):
        """Get available job categories for Indeed"""
        return self.JOB_CATEGORIES
    
    def get_job_types(self):
        """Get available job types for Indeed"""
        return self.JOB_TYPES
    
    async def search_jobs(self, location, radius, categories=None, job_types=None):
        """Search for jobs on Indeed API"""
        print(f"[Indeed] Searching for jobs in {location} within {radius}km")
        
        if not self.publisher_id:
            print("[Indeed] Publisher ID not configured")
            return []
        
        # Convert radius from km to miles (Indeed uses miles)
        radius_miles = int(radius * 0.621371)
        if radius_miles < 5:
            radius_miles = 5  # Minimum 5 miles
            
        # Build Indeed API URL with filters
        params = {
            'publisher': self.publisher_id,
            'format': 'json',
            'v': '2',
            'limit': 25,  # Max 25 results per request
            'l': location,  # Location
            'radius': radius_miles,
            'sort': 'date',
            'fromage': 30  # Last 30 days
        }
        
        # Add keyword filters for categories
        if categories and len(categories) > 0:
            # Use the first category as a keyword
            category = categories[0].replace(" Jobs", "")
            params['q'] = category
        
        # Add job type filter
        if job_types and len(job_types) > 0:
            # Map our job type to Indeed job type
            for job_type in job_types:
                # Find matching Indeed job type
                for indeed_type, our_type in self.JOB_TYPE_MAPPING.items():
                    if our_type == job_type:
                        params['jt'] = indeed_type
                        break
        
        print(f"[Indeed] API params: {json.dumps(params)}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status != 200:
                        print(f"[Indeed] API error: {response.status}")
                        return []
                    
                    data = await response.json()
                    results = data.get('results', [])
                    
                    print(f"[Indeed] Found {len(results)} jobs")
                    
                    # Convert to standard format
                    return [self.standardize_job(job) for job in results]
        except Exception as e:
            print(f"[Indeed] Error searching jobs: {str(e)}")
            return []
    
    def standardize_job(self, job_data):
        """Convert Indeed job data to standard format"""
        # Parse date
        date_posted = None
        if 'date' in job_data:
            try:
                date_posted = job_data['date']
            except:
                pass
        
        # Extract salary if available
        salary_min = None
        salary_max = None
        currency = "GBP"
        
        if 'salary' in job_data and job_data['salary']:
            salary_text = job_data['salary']
            # Try to extract numerical values
            import re
            numbers = re.findall(r'\d+(?:,\d+)*(?:\.\d+)?', salary_text)
            if len(numbers) >= 2:
                # Assume first is min, second is max
                try:
                    salary_min = float(numbers[0].replace(',', ''))
                    salary_max = float(numbers[1].replace(',', ''))
                except:
                    pass
            elif len(numbers) == 1:
                # Single number - could be annual or hourly
                try:
                    value = float(numbers[0].replace(',', ''))
                    if value < 100:  # Likely hourly
                        # Convert to annual (assuming 40hr week, 52 weeks)
                        value = value * 40 * 52
                    salary_min = value
                    salary_max = value * 1.2  # Estimate max as 20% higher
                except:
                    pass
            
            # Detect currency
            if '£' in salary_text:
                currency = "GBP"
            elif '€' in salary_text:
                currency = "EUR"
            elif '$' in salary_text:
                # Look for context to determine USD, CAD, AUD, etc.
                if any(x in salary_text.lower() for x in ['us', 'usa', 'united states']):
                    currency = "USD"
                else:
                    currency = "USD"  # Default to USD
        
        # Determine category based on job title and description
        category = "Unknown"
        job_title = job_data.get('jobtitle', '')
        job_snippet = job_data.get('snippet', '')
        
        for cat in self.JOB_CATEGORIES:
            cat_name = cat.replace(' Jobs', '').lower()
            if cat_name in job_title.lower() or cat_name in job_snippet.lower():
                category = cat
                break
        
        # Determine job type
        contract_type = "Unknown"
        if 'jobtype' in job_data:
            indeed_job_type = job_data['jobtype'].lower().replace(' ', '')
            if indeed_job_type in self.JOB_TYPE_MAPPING:
                contract_type = self.JOB_TYPE_MAPPING[indeed_job_type]
        
        return {
            "id": job_data.get('jobkey', f"indeed-{datetime.now().timestamp()}"),
            "title": job_data.get('jobtitle', 'Unknown Position'),
            "company": {
                "display_name": job_data.get('company', 'Unknown')
            },
            "location": {
                "area": [job_data.get('city', 'Unknown'), job_data.get('country', 'Unknown')]
            },
            "description": job_data.get('snippet', 'No description available'),
            "redirect_url": job_data.get('url', ''),
            "source_api": self.name,
            "latitude": job_data.get('latitude'),
            "longitude": job_data.get('longitude'),
            "category": {
                "label": category
            },
            "contract_type": contract_type,
            "created": date_posted,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "currency": currency,
            "company_metadata": {
                "address": job_data.get('formattedLocation', 'N/A'),
                "phone": 'N/A',
                "website": 'N/A',
                "maps_url": 'N/A'
            }
        } 