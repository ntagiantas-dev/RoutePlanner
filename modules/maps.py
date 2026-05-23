import requests
import folium
import streamlit as st

def geocode_address(address, api_key):
    url = "https://api.geoapify.com/v1/geocode/search"
    params = {"text": address, "apiKey": api_key}
    response = requests.get(url, params=params)
    data = response.json()
    if data["features"]:
        lon = data["features"][0]["geometry"]["coordinates"][0]
        lat = data["features"][0]["geometry"]["coordinates"][1]
        return lat, lon
    return None, None

def optimize_route(addresses, api_key):
    # Βήμα 1: Geocoding
    coords = []
    for address in addresses:
        lat, lon = geocode_address(address, api_key)
        if lat and lon:
            coords.append({"address": address, "lat": lat, "lon": lon})

    if len(coords) < 2:
        return coords, 0

    # Βήμα 2: Route Optimization
    url = "https://api.geoapify.com/v1/routeplanner"
    
    payload = {
        "mode": "drive",
        "agents": [{
            "start_location": [coords[0]["lon"], coords[0]["lat"]],
            "end_location": [coords[-1]["lon"], coords[-1]["lat"]]
        }],
        "jobs": [
            {
                "id": i,
                "location": [c["lon"], c["lat"]]
            }
            for i, c in enumerate(coords[1:-1])
        ]
    }
    
    response = requests.post(
        url,
        json=payload,
        params={"apiKey": api_key}
    )
    data = response.json()
    
    try:
        waypoints = data["features"][0]["properties"]["waypoints"]
        ordered = [coords[0]]
        for wp in waypoints:
            job_id = wp["original_location_index"]
            ordered.append(coords[job_id + 1])
        ordered.append(coords[-1])
        total_time = data["features"][0]["properties"]["time"]
        return ordered, total_time
    except:
        return coords, 0

def create_map(stops):
    if not stops:
        return None
    m = folium.Map(location=[stops[0]["lat"], stops[0]["lon"]], zoom_start=13)
    for i, stop in enumerate(stops):
        if stop.get("status") == "done":
            color = "green"
        elif stop.get("status") == "skip":
            color = "gray"
        else:
            color = "red"
        folium.Marker(
            location=[stop["lat"], stop["lon"]],
            popup=f"{i+1}. {stop['address']}",
            icon=folium.Icon(color=color)
        ).add_to(m)
    return m

def get_google_maps_url(address):
    address_encoded = address.replace(" ", "+")
    return f"https://www.google.com/maps/dir/?api=1&destination={address_encoded}"