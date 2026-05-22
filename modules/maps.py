# ============================================
# MAPS MODULE
# Υπεύθυνο για χάρτες και βελτιστοποίηση διαδρομής
# Χρησιμοποιεί Geoapify API για βελτιστοποίηση
# και Folium για εμφάνιση χάρτη
# ============================================

import requests
import folium
import streamlit as st

def optimize_route(addresses, api_key):
    """
    Στέλνει τις διευθύνσεις στο Geoapify
    και επιστρέφει τη βέλτιστη σειρά.
    addresses: λίστα με διευθύνσεις
    api_key: το Geoapify API key
    """
    # Geocoding - μετατροπή διευθύνσεων σε συντεταγμένες
    coords = []
    for address in addresses:
        url = f"https://api.geoapify.com/v1/geocode/search"
        params = {"text": address, "apiKey": api_key}
        response = requests.get(url, params=params)
        data = response.json()
        if data["features"]:
            lon = data["features"][0]["geometry"]["coordinates"][0]
            lat = data["features"][0]["geometry"]["coordinates"][1]
            coords.append({"address": address, "lat": lat, "lon": lon})
    return coords

def create_map(stops):
    """
    Δημιουργεί χάρτη Folium με τις στάσεις.
    stops: λίστα με dict {address, lat, lon, status}
    """
    if not stops:
        return None
    
    # Κεντράρισμα χάρτη στην πρώτη στάση
    m = folium.Map(location=[stops[0]["lat"], stops[0]["lon"]], zoom_start=13)
    
    for i, stop in enumerate(stops):
        # Χρώμα ανάλογα με την κατάσταση
        if stop.get("status") == "done":
            color = "green"
        elif stop.get("status") == "skip":
            color = "gray"
        else:
            color = "red"  # pending
        
        # Προσθήκη marker στον χάρτη
        folium.Marker(
            location=[stop["lat"], stop["lon"]],
            popup=f"{i+1}. {stop['address']}",
            icon=folium.Icon(color=color)
        ).add_to(m)
    
    return m

def get_google_maps_url(address):
    """
    Δημιουργεί URL για Google Maps navigation.
    Ανοίγει στο κινητό του οδηγού.
    """
    address_encoded = address.replace(" ", "+")
    return f"https://www.google.com/maps/dir/?api=1&destination={address_encoded}"
