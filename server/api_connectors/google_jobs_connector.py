import os
import aiohttp
import json
from datetime import datetime
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.oauth2 import service_account
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
        
        # Create credentials for service
        self.credentials = self._get_credentials()
        
        # Google Cloud Talent Solution API endpoint for HTTP requests
        self.base_url = f"https://jobs.googleapis.com/v4/projects/{self.project_id}/tenants/default/jobs:search"
    
    def _get_credentials(self):
        """Create Google OAuth2 credentials object"""
        try:
            # If service account credentials exist, use them
            if os.path.exists('service-account.json'):
                return service_account.Credentials.from_service_account_file(
                    'service-account.json',
                    scopes=['https://www.googleapis.com/auth/jobs']
                )
            # Otherwise use client credentials
            elif self.client_id and self.client_secret:
                # For simplicity in this app, we're using a basic credential
                # In a production app, you'd implement a proper OAuth flow with refresh tokens
                return google.oauth2.credentials.Credentials(
                    None,  # No access token needed for this basic approach
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    token_uri=os.getenv('GOOGLE_TOKEN_URI')
                )
            return None
        except Exception as e:
            print(f"Error creating Google credentials: {str(e)}")
            return None
    
    def get_categories(self):
        """Get available job categories for Google Jobs"""
        return self.JOB_CATEGORIES
    
    def get_job_types(self):
        """Get available job types for Google Jobs"""
        return self.JOB_TYPES
    
    async def search_jobs(self, location, radius, categories=None, job_types=None):
        """Search for jobs on Google Jobs API"""
        print(f"[GoogleJobs] Searching for jobs in {location} within {radius}km")
        
        if not self.credentials or not self.project_id:
            print("[GoogleJobs] Credentials or project ID not configured")
            return []
            
        # Prepare request body for Google Jobs API
        request_body = {
            "searchMode": "JOB_SEARCH",
            "requestMetadata": {
                "userId": "user-id",
                "sessionId": "session-id",
                "domain": "companyhunter.com"
            },
            "jobQuery": {
                "locationFilters": [
                    {
                        "address": location,
                        "distanceInKm": radius
                    }
                ],
                "query": ""
            },
            "pageSize": 100
        }
        
        # Add job category filter if provided
        if categories and len(categories) > 0:
            # Build a combined query for categories
            query_parts = []
            for category in categories:
                # Remove "Jobs" suffix if present for better matching
                if category.endswith(" Jobs"):
                    category = category[:-5]
                query_parts.append(category)
            
            if query_parts:
                request_body["jobQuery"]["query"] = " OR ".join(query_parts)
        
        # Add job type filter if provided
        if job_types and len(job_types) > 0:
            # Convert our standard job types to Google's format
            google_job_types = []
            for job_type in job_types:
                for google_type, our_type in self.JOB_TYPE_MAPPING.items():
                    if our_type == job_type:
                        google_job_types.append(google_type)
            
            if google_job_types:
                request_body["jobQuery"]["employmentTypes"] = google_job_types
        
        print(f"[GoogleJobs] Request body: {json.dumps(request_body)}")
        
        try:
            # Build the service
            talent_service = googleapiclient.discovery.build(
                'jobs', 'v4', credentials=self.credentials)
            
            # Make the API request
            search_jobs_request = {
                'parent': f'projects/{self.project_id}/tenants/default',
                'requestMetadata': {
                    'userId': 'user-id',
                    'sessionId': 'session-id',
                    'domain': 'companyhunter.com'
                },
                'jobQuery': {
                    'locationFilters': [
                        {
                            'address': location,
                            'distanceInKm': radius
                        }
                    ],
                    'query': request_body["jobQuery"].get("query", "")
                },
                'pageSize': 100
            }
            
            # Add employment types if provided
            if "employmentTypes" in request_body["jobQuery"]:
                search_jobs_request["jobQuery"]["employmentTypes"] = request_body["jobQuery"]["employmentTypes"]
                
            response = talent_service.projects().tenants().jobs().search(
                parent=f'projects/{self.project_id}/tenants/default',
                body=search_jobs_request
            ).execute()
            
            jobs = response.get('matchingJobs', [])
            print(f"[GoogleJobs] Found {len(jobs)} jobs")
            
            # Convert to standard format
            return [self.standardize_job(job.get('job', {})) for job in jobs]
            
        except Exception as e:
            print(f"[GoogleJobs] Error searching jobs: {str(e)}")
            return []
    
    def standardize_job(self, job_data):
        """Convert Google Jobs data to standard format"""
        # Extract company information
        company_name = job_data.get('company', 'Unknown')
        if isinstance(company_name, dict) and 'name' in company_name:
            company_name = company_name.get('name', 'Unknown')
        
        # Extract job title
        title = job_data.get('title', 'Unknown Position')
        
        # Extract job location
        location_data = job_data.get('locations', [{}])[0] if job_data.get('locations') else {}
        location_str = location_data.get('address', 'Unknown') if isinstance(location_data, dict) else str(location_data)
        location_parts = location_str.split(',')
        
        # Extract coordinates
        coordinates = None
        if isinstance(location_data, dict) and 'latLng' in location_data:
            lat_lng = location_data.get('latLng', {})
            if 'latitude' in lat_lng and 'longitude' in lat_lng:
                coordinates = {
                    'latitude': lat_lng.get('latitude'),
                    'longitude': lat_lng.get('longitude')
                }
        
        # Extract description
        description = job_data.get('description', 'No description available')
        
        # Extract job type
        job_type = "Unknown"
        employment_types = job_data.get('employmentTypes', [])
        if employment_types and len(employment_types) > 0:
            google_type = employment_types[0]
            job_type = self.JOB_TYPE_MAPPING.get(google_type, "Unknown")
        
        # Extract salary
        compensation = job_data.get('compensationInfo', {})
        salary_min = None
        salary_max = None
        currency = "USD"  # Default
        
        if compensation:
            ranges = compensation.get('entries', [])
            if ranges and len(ranges) > 0:
                salary_range = ranges[0]
                if 'min' in salary_range and 'units' in salary_range['min']:
                    salary_min = int(salary_range['min']['units'])
                if 'max' in salary_range and 'units' in salary_range['max']:
                    salary_max = int(salary_range['max']['units'])
                if 'currencyCode' in salary_range:
                    currency = salary_range['currencyCode']
        
        # Extract posting date
        created_date = None
        if 'postingPublishTime' in job_data:
            try:
                # Google uses RFC3339 format
                created_date = job_data['postingPublishTime']
            except:
                pass
        
        # Extract application URL
        application_url = None
        if 'applicationInfo' in job_data and 'uris' in job_data['applicationInfo']:
            uris = job_data['applicationInfo']['uris']
            if uris and len(uris) > 0:
                application_url = list(uris.values())[0]
        
        # Determine category based on title and description
        category = "IT Jobs"  # Default
        for cat in self.JOB_CATEGORIES:
            cat_name = cat.replace(' Jobs', '')
            if cat_name.lower() in title.lower() or cat_name.lower() in description.lower():
                category = cat
                break
        
        # Get company website
        company_website = None
        if 'company' in job_data and isinstance(job_data['company'], dict):
            if 'websiteUri' in job_data['company']:
                company_website = job_data['company']['websiteUri']
        
        return {
            "title": title,
            "company": {
                "display_name": company_name
            },
            "location": {
                "area": location_parts
            },
            "description": description,
            "redirect_url": application_url or "",
            "source_api": self.name,
            "latitude": coordinates['latitude'] if coordinates else None,
            "longitude": coordinates['longitude'] if coordinates else None,
            "category": {
                "label": category
            },
            "contract_type": job_type,
            "created": created_date,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "currency": currency,
            "company_metadata": {
                "address": location_str,
                "phone": "N/A",
                "website": company_website or "N/A",
                "maps_url": "N/A"
            }
        } 