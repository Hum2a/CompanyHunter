#WIP. [1/2] Needs optimisation/a total rewrite. Works though. Needs to be hooked into program.

# Originally a console program that took in and output json files, since that'd be a bit of a pain to do largescale, just have it output an array of objects (companies), I've already defined the objects in here too
# To add:
# [ ] blacklist
# [ ] get long/lat or postcode from node ID (if cna't find address or email, need to contact google company API and retrieve from there)
# [X] Ammended to now take in a list of (postcode, radius) and output a list of office objects (see line 62)

import json
import requests
import os

HEADERS = {
    "User-Agent": "CompanySearcher/1.1 (CompanyHunter1.0)"
}

def process_areas(area_list):
    all_offices = []
    for postcode, radius in area_list:
        offices = process_area(postcode, radius)
        all_offices.extend(offices)
    return all_offices

def process_area(postcode, radius):
    lat, lon = get_coordinates_from_postcode(postcode)
    if lat == 0 and lon == 0:
        print(f"Invalid postcode: {postcode}")
        return []
    print(f"Searching for offices in {postcode} ({lat}, {lon}) within {radius} meters...")
    return get_offices(lat, lon, radius)

def get_coordinates_from_postcode(postcode):
    url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(postcode)}, UK&format=json"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Error: Unable to fetch coordinates for {postcode}")
        return 0, 0
    
    locations = response.json()
    if locations:
        return float(locations[0]["lat"]), float(locations[0]["lon"])
    
    print(f"Error: No coordinates found for {postcode}")
    return 0, 0

def get_offices(lat, lon, radius):
    query = f"[out:json];(way[\"office\"](around:{radius},{lat},{lon});node[\"office\"](around:{radius},{lat},{lon});relation[\"office\"](around:{radius},{lat},{lon}););out center;"
    url = f"https://overpass-api.de/api/interpreter?data={query}"
    
    print("Fetching from Overpass API...")
    print("URL:", url)
    
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200 or not response.text.strip():
            print("Error: Empty response from Overpass API.")
            return []
        
        result = response.json()
        elements = result.get("elements", [])
        
        offices = []
        for e in elements:
            office = {
                "id": e["id"],
                "name": e.get("tags", {}).get("name", "N/A"),
                "type": e.get("tags", {}).get("office", "N/A"),
                "lat": e.get("lat", e.get("center", {}).get("lat", 0)),
                "lon": e.get("lon", e.get("center", {}).get("lon", 0)),
                "tags": {k: v for k, v in e.get("tags", {}).items() if k not in ["office", "name"]}
            }
            if office["lat"] != 0 and office["lon"] != 0:
                offices.append(office)
        
        print(f"Found {len(offices)} offices!")
        return offices
    except requests.RequestException as e:
        print(f"HTTP Request Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    return []

