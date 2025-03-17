import os
import aiohttp
import json
from datetime import datetime
from .base_connector import BaseJobConnector

class GitHubJobsConnector(BaseJobConnector):
    """Connector for the GitHub Jobs API (Discontinued)"""
    
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
        "full_time",
        "contract",
        "remote"
    ]
    
    def __init__(self):
        super().__init__()
        self.name = "GitHub Jobs"
        # Note: The GitHub Jobs API was discontinued in May 2021
    
    def get_categories(self):
        """Get available job categories for GitHub Jobs"""
        return self.JOB_CATEGORIES
    
    def get_job_types(self):
        """Get available job types for GitHub Jobs"""
        return self.JOB_TYPES
    
    async def search_jobs(self, location, radius, categories=None, job_types=None):
        """Return dummy GitHub Jobs data since the API is discontinued"""
        print(f"[GitHub] GitHub Jobs API is discontinued. Returning dummy data for {location}")
        
        # Return dummy jobs based on location and categories
        dummy_jobs = []
        
        # Create some tech company dummy jobs
        companies = ["GitHub", "Microsoft", "Meta", "Apple", "Amazon"]
        titles = ["Software Engineer", "Full Stack Developer", "DevOps Engineer", 
                 "Data Scientist", "Product Manager", "QA Engineer"]
        
        # Filter by category if provided
        filtered_titles = titles
        if categories and len(categories) > 0:
            filtered_titles = []
            for title in titles:
                for category in categories:
                    cat_name = category.replace(" Jobs", "").lower()
                    if cat_name in title.lower():
                        filtered_titles.append(title)
                        break
            
            # If no matches, use all titles
            if not filtered_titles:
                filtered_titles = titles
        
        # Create 2-3 random jobs
        for i in range(min(3, len(companies))):
            company = companies[i]
            title = filtered_titles[i % len(filtered_titles)]
            
            # Create a job with different contract type based on job_types filter
            contract_type = "full_time"  # Default
            if job_types and len(job_types) > 0:
                contract_type = job_types[0]  # Use the first job type
            
            dummy_jobs.append(self._create_dummy_job(location, company, title, contract_type))
        
        return dummy_jobs
    
    def _create_dummy_job(self, location, company, title, contract_type):
        """Create a dummy job with the given parameters"""
        # Determine category based on title
        category = "Software Development Jobs"  # Default
        if "data" in title.lower():
            category = "Data Science Jobs"
        elif "devops" in title.lower():
            category = "DevOps Jobs"
        elif "full stack" in title.lower() or "frontend" in title.lower() or "backend" in title.lower():
            category = "Web Development Jobs"
        
        # Parse location into city/country
        location_parts = location.split(',')
        city = location_parts[0].strip() if location_parts else 'Unknown'
        country = location_parts[-1].strip() if len(location_parts) > 1 else 'UK'
        
        # Create salary based on title and company
        base_salary = 70000
        if "senior" in title.lower():
            base_salary += 40000
        elif "lead" in title.lower() or "manager" in title.lower():
            base_salary += 60000
        
        if company in ["Google", "Apple", "Meta", "Amazon"]:
            base_salary += 20000
        
        salary_min = base_salary
        salary_max = base_salary + 30000
        
        return {
            "id": f"github-{company.lower()}-{datetime.now().timestamp()}",
            "title": title,
            "company": {
                "display_name": company
            },
            "location": {
                "area": [city, country]
            },
            "description": f"This is a dummy {title} position at {company}, created because GitHub Jobs API has been discontinued. The role involves working on cutting-edge technologies in a collaborative environment.",
            "redirect_url": f"https://{company.lower()}.com/careers",
            "source_api": self.name,
            "latitude": None,  # GitHub Jobs doesn't provide coordinates
            "longitude": None,
            "category": {
                "label": category
            },
            "contract_type": contract_type,
            "created": datetime.now().isoformat(),
            "salary_min": salary_min,
            "salary_max": salary_max,
            "currency": "GBP",
            "company_metadata": {
                "address": f"{company} Office, {location}",
                "phone": "N/A",
                "website": f"https://{company.lower()}.com",
                "maps_url": "N/A"
            }
        } 