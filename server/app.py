from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import math
import json
import asyncio
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Import API connectors
from api_connectors import (
    AdzunaConnector, 
    ReedConnector, 
    GitHubJobsConnector, 
    GoogleJobsConnector,
    IndeedConnector,
    JobAggregator
)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# API keys
ADZUNA_APP_ID = os.getenv('ADZUNA_APP_ID')
ADZUNA_API_KEY = os.getenv('ADZUNA_API_KEY')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
REED_API_KEY = os.getenv('REED_API_KEY')
INDEED_PUBLISHER_ID = os.getenv('INDEED_PUBLISHER_ID')

# Google OAuth credentials
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_PROJECT_ID = os.getenv('GOOGLE_PROJECT_ID')

# Blacklist of companies to filter out
COMPANY_BLACKLIST = []

# Initialize job aggregator with all connectors
job_aggregator = JobAggregator()

# Add connectors if API keys are available
if ADZUNA_APP_ID and ADZUNA_API_KEY:
    print("Adding Adzuna connector")
    try:
        job_aggregator.add_connector(AdzunaConnector(ADZUNA_APP_ID, ADZUNA_API_KEY))
        print(f"Adzuna credentials: app_id={ADZUNA_APP_ID[:5]}... app_key={ADZUNA_API_KEY[:5]}...")
    except Exception as e:
        print(f"Error initializing Adzuna connector: {str(e)}")
else:
    print("Adzuna API keys not found, skipping connector")

if REED_API_KEY and REED_API_KEY != "your_reed_api_key_here":
    print("Adding Reed connector")
    try:
        job_aggregator.add_connector(ReedConnector(REED_API_KEY))
    except Exception as e:
        print(f"Error initializing Reed connector: {str(e)}")
else:
    print("Reed API key not found or is a placeholder, skipping connector")

# Add Indeed connector if Publisher ID is available
if INDEED_PUBLISHER_ID and INDEED_PUBLISHER_ID != "your_indeed_publisher_id_here":
    print("Adding Indeed connector")
    try:
        job_aggregator.add_connector(IndeedConnector(INDEED_PUBLISHER_ID))
        print(f"Indeed Publisher ID: {INDEED_PUBLISHER_ID[:5]}...")
    except Exception as e:
        print(f"Error initializing Indeed connector: {str(e)}")
else:
    print("Indeed Publisher ID not found or is a placeholder, skipping connector")

# Google Jobs API requires OAuth credentials and project ID
if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET and GOOGLE_PROJECT_ID:
    print("Adding Google Jobs connector with OAuth")
    job_aggregator.add_connector(GoogleJobsConnector(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        project_id=GOOGLE_PROJECT_ID
    ))
else:
    print("Google OAuth credentials or project ID not found, skipping connector")

# GitHub Jobs doesn't need API keys
print("Adding GitHub Jobs connector")
job_aggregator.add_connector(GitHubJobsConnector())

# Get combined categories and job types
ALL_CATEGORIES = job_aggregator.get_categories()
ALL_JOB_TYPES = job_aggregator.get_job_types()

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in kilometers"""
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    
    return c * r

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all available job categories"""
    return jsonify(ALL_CATEGORIES)

@app.route('/api/job_types', methods=['GET'])
def get_job_types():
    """Get all available job types"""
    return jsonify(ALL_JOB_TYPES)

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get jobs within radius of location using multiple APIs"""
    # Get query parameters
    location = request.args.get('location', '')
    radius = float(request.args.get('radius', 10))  # default 10km
    categories = request.args.getlist('category')  # Multiple categories can be selected
    job_types = request.args.getlist('job_type')   # Multiple job types can be selected
    
    print(f"Requested location: {location}")
    print(f"Requested radius: {radius}")
    print(f"Requested categories: {categories}")
    print(f"Requested job types: {job_types}")
    
    if not location:
        return jsonify({'error': 'Location is required'}), 400
    
    try:
        # Get coordinates for location using Google Maps API
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_MAPS_API_KEY}"
        print(f"Geocoding URL: {geocode_url}")
        geocode_response = requests.get(geocode_url)
        geocode_data = geocode_response.json()
        
        print(f"Geocode response status: {geocode_data['status']}")
        
        if geocode_data['status'] != 'OK':
            return jsonify({'error': 'Could not geocode location'}), 400
        
        # Extract coordinates
        coordinates = geocode_data['results'][0]['geometry']['location']
        lat = coordinates['lat']
        lng = coordinates['lng']
        
        # Get formatted address for the search area
        formatted_address = geocode_data['results'][0].get('formatted_address', '')
        print(f"Formatted address: {formatted_address}")
        
        # Create the event loop and run the aggregator search
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        all_jobs = loop.run_until_complete(
            job_aggregator.search_jobs(
                location=formatted_address,
                radius=radius,
                categories=categories if categories else None,
                job_types=job_types if job_types else None
            )
        )
        loop.close()
        
        # Post-process to filter out blacklisted companies and apply distance filter
        filtered_jobs = []
        for job in all_jobs:
            # Skip if company is in blacklist
            company_name = job.get('company', {}).get('display_name', '')
            if company_name in COMPANY_BLACKLIST:
                print(f"Company {company_name} is blacklisted, skipping")
                continue
            
            # Handle jobs without location data or distance calculation
            job_lat = job.get('latitude')
            job_lng = job.get('longitude')
            
            # If no coordinates or distance, add it with distance 0
            if not job_lat or not job_lng or 'distance' not in job:
                job_lat = lat
                job_lng = lng
                job['distance'] = 0
                job['latitude'] = job_lat
                job['longitude'] = job_lng
            
            # Override distance calculation if needed (some APIs provide this)
            if 'distance' not in job:
                distance = calculate_distance(lat, lng, job_lat, job_lng)
                job['distance'] = distance
            
            # Skip if outside radius
            if job['distance'] > radius:
                continue
                
            # Get additional metadata from Google Maps if needed
            if (not job.get('company_metadata') or 
                all(value == 'N/A' for value in job.get('company_metadata', {}).values())):
                try:
                    if company_name:
                        print(f"Getting additional metadata for company: {company_name}")
                        # Add location context to improve search accuracy
                        search_query = f"{company_name} {formatted_address}"
                        places_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={search_query}&inputtype=textquery&fields=formatted_address,name,rating,opening_hours,geometry,place_id&key={GOOGLE_MAPS_API_KEY}"
                        places_response = requests.get(places_url)
                        places_data = places_response.json()
                        
                        if places_data['status'] == 'OK' and places_data.get('candidates'):
                            place_id = places_data['candidates'][0]['place_id']
                            
                            # Get place details
                            details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_address,formatted_phone_number,website,url&key={GOOGLE_MAPS_API_KEY}"
                            details_response = requests.get(details_url)
                            details_data = details_response.json()
                            
                            if details_data['status'] == 'OK':
                                details = details_data['result']
                                
                                # Initialize metadata if not present
                                if 'company_metadata' not in job:
                                    job['company_metadata'] = {
                                        'address': 'N/A',
                                        'phone': 'N/A',
                                        'website': 'N/A',
                                        'maps_url': 'N/A'
                                    }
                                
                                # Update metadata with Google data (only if present)
                                if details.get('formatted_address'):
                                    job['company_metadata']['address'] = details.get('formatted_address')
                                
                                if details.get('formatted_phone_number'):
                                    job['company_metadata']['phone'] = details.get('formatted_phone_number')
                                
                                if details.get('website'):
                                    job['company_metadata']['website'] = details.get('website')
                                
                                if details.get('url'):
                                    job['company_metadata']['maps_url'] = details.get('url')
                except Exception as e:
                    print(f"Error getting company metadata: {str(e)}")
            
            # Add to filtered jobs
            filtered_jobs.append(job)
        
        print(f"Total filtered jobs: {len(filtered_jobs)}")
        
        return jsonify({
            'total': len(filtered_jobs),
            'results': filtered_jobs,
            'coordinates': {
                'latitude': lat,
                'longitude': lng
            }
        })
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/save', methods=['POST'])
def save_company():
    """Save a company to favorites"""
    try:
        data = request.json
        # TODO: Implement saving to database
        return jsonify({'success': True, 'message': 'Company saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
