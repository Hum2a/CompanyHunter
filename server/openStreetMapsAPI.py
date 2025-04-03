#WIP. [ ] Needs optimisation/a total rewrite. Works though. Needs to be hooked into program.

# Originally a console program that took in and output json files, since that'd be a bit of a pain to do largescale, just have it output an array of objects (companies), I've already defined the objects in here too
# To add: blacklist, 

import json
import requests
import os

JSON_FILE_PATH = "companies.json"
HEADERS = {
    "User-Agent": "CompanySearch/1.0 (CompanyHunter1.0)"
}

def main():
    while True:
        choice = "1"

        if choice == "1":
            postcode = input("Enter postcode: ")
            radius = int(input("Enter radius (meters): "))
            process_area(postcode, radius)
        elif choice == "2": #<--- multiple paths check
            path = input("Enter path to areas JSON: ")
            load_areas_from_json(path)

def process_area(postcode, radius):
    lat, lon = get_coordinates_from_postcode(postcode)
    if lat == 0 and lon == 0:
        print("Invalid postcode. Please try again.")
        return
    print(f"Searching for offices in {postcode} ({lat}, {lon}) within {radius} meters...")
    
    new_offices = get_offices(lat, lon, radius)
    existing_offices = load_existing_offices()

    for office in new_offices:
        if not any(o['id'] == office['id'] for o in existing_offices):
            existing_offices.append(office)

    print("Offices added successfully.")
    ##Set up to return array of offices here!

def load_areas_from_json(path):
    if not os.path.exists(path):
        print("File not found.")
        return
    
    with open(path, "r") as file:
        areas = json.load(file)
    
    for area in areas:
        process_area(area["Postcode"], area["Radius"])

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

def load_existing_offices():
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, "r") as file:
            return json.load(file)
    return []

if __name__ == "__main__":
    main()
