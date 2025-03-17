from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import math
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# API keys
ADZUNA_APP_ID = os.getenv('ADZUNA_APP_ID')
ADZUNA_API_KEY = os.getenv('ADZUNA_API_KEY')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# Blacklist of companies to filter out
COMPANY_BLACKLIST = []

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    # Earth radius in kilometers
    R = 6371.0
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get jobs within radius of location"""
    # Get query parameters
    location = request.args.get('location', '')
    radius = float(request.args.get('radius', 10))  # default 10km
    
    if not location:
        return jsonify({'error': 'Location is required'}), 400
    
    try:
        # Get coordinates for location using Google Maps API
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_MAPS_API_KEY}"
        geocode_response = requests.get(geocode_url)
        geocode_data = geocode_response.json()
        
        if geocode_data['status'] != 'OK':
            return jsonify({'error': 'Could not geocode location'}), 400
        
        # Extract coordinates
        coordinates = geocode_data['results'][0]['geometry']['location']
        lat = coordinates['lat']
        lng = coordinates['lng']
        
        # Get formatted address for the search area
        formatted_address = geocode_data['results'][0].get('formatted_address', '')
        
        # Extract country, city, region from formatted_address for better Adzuna search
        address_parts = formatted_address.split(',')
        
        # Determine the most relevant location parts for search
        search_location = address_parts[0].strip() if address_parts else location
        
        # Use a larger search radius for Adzuna to ensure we get results
        api_radius = int(radius * 2)  # Double the radius for the API search
        if api_radius < 10:
            api_radius = 10  # Minimum 10km for API search
            
        # Get jobs from Adzuna API with broader search
        # Don't use the what_and parameter which is too restrictive
        # Instead use where parameter and distance search from the API
        adzuna_url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_API_KEY}&results_per_page=100&where={search_location}&distance={api_radius}"
        
        print(f"Adzuna API URL: {adzuna_url}")  # Debug log
        
        adzuna_response = requests.get(adzuna_url)
        adzuna_data = adzuna_response.json()
        
        print(f"Adzuna API response status: {adzuna_response.status_code}")  # Debug log
        print(f"Total results from Adzuna: {adzuna_data.get('count', 0)}")  # Debug log
        
        # If no results in first page, try a more generic search
        if not adzuna_data.get('results'):
            # Try a more generic search without specific location
            adzuna_url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_API_KEY}&results_per_page=100"
            adzuna_response = requests.get(adzuna_url)
            adzuna_data = adzuna_response.json()
            print(f"Fallback search - total results: {adzuna_data.get('count', 0)}")  # Debug log
        
        # Filter jobs by distance and blacklist
        filtered_jobs = []
        for job in adzuna_data.get('results', []):
            # Skip if company is in blacklist
            company = job.get('company', {}).get('display_name', '')
            if company in COMPANY_BLACKLIST:
                continue
            
            # Handle jobs without location data
            job_lat = job.get('latitude')
            job_lng = job.get('longitude')
            
            # If the job doesn't have coordinates, use the search coordinates
            # This allows us to include jobs without precise coordinates
            if not job_lat or not job_lng:
                job_lat = lat
                job_lng = lng
                distance = 0  # Assume it's at the center of search
            else:
                # Calculate distance
                distance = calculate_distance(lat, lng, job_lat, job_lng)
            
            # Skip if outside radius
            if distance > radius:
                continue
            
            # Get company metadata from Google Maps
            try:
                company_name = job.get('company', {}).get('display_name', '')
                if company_name:
                    places_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={company_name}&inputtype=textquery&fields=formatted_address,name,rating,opening_hours,geometry,place_id&key={GOOGLE_MAPS_API_KEY}"
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
                            
                            # Add metadata to job
                            job['company_metadata'] = {
                                'address': details.get('formatted_address', 'N/A'),
                                'phone': details.get('formatted_phone_number', 'N/A'),
                                'website': details.get('website', 'N/A'),
                                'maps_url': details.get('url', 'N/A')
                            }
                    else:
                        # If no place found, set default metadata
                        job['company_metadata'] = {
                            'address': 'N/A',
                            'phone': 'N/A',
                            'website': 'N/A',
                            'maps_url': 'N/A'
                        }
            except Exception as e:
                print(f"Error getting company metadata: {str(e)}")
                # If company metadata retrieval fails, continue with N/A values
                job['company_metadata'] = {
                    'address': 'N/A',
                    'phone': 'N/A',
                    'website': 'N/A',
                    'maps_url': 'N/A'
                }
            
            # Add distance to job
            job['distance'] = distance
            
            # Add to filtered jobs
            filtered_jobs.append(job)
        
        print(f"Total filtered jobs: {len(filtered_jobs)}")  # Debug log
        
        return jsonify({
            'total': len(filtered_jobs),
            'results': filtered_jobs
        })
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/save', methods=['POST'])
def save_company():
    """Save company data"""
    company_data = request.json
    
    if not company_data:
        return jsonify({'error': 'No data provided'}), 400
    
    # In a real app, you would save this to a database
    # For now, we'll just return success
    return jsonify({'success': True, 'message': 'Company saved'})

if __name__ == '__main__':
    app.run(debug=True)
