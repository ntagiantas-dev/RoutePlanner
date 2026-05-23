# ============================================
# ROUTES MODULE
# Υπεύθυνο για τη διαχείριση των διαδρομών
# Κάθε route έχει στάσεις με status:
# pending = εκκρεμεί, done = ολοκληρώθηκε, skip = παραλείφθηκε
# ============================================

import streamlit as st
from modules.database import get_all_routes, save_route
from modules.maps import get_google_maps_url
import uuid
from datetime import datetime

def create_route(driver_username, stops, optimized_stops=None):
    """
    Δημιουργεί νέο route για οδηγό.
    driver_username: το όνομα του οδηγού
    stops: λίστα διευθύνσεων
    optimized_stops: λίστα με dict {address, lat, lon} από Geoapify
    """
    if optimized_stops:
        stops_data = [
            {
                "address": s["address"],
                "status": "pending",
                "lat": s["lat"],
                "lon": s["lon"]
            }
            for s in optimized_stops
        ]
    else:
        stops_data = [
            {
                "address": addr,
                "status": "pending",
                "lat": None,
                "lon": None
            }
            for addr in stops
        ]

    route = {
        "id": str(uuid.uuid4()),
        "driver": driver_username,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "active",
        "stops": stops_data
    }
    save_route(route)
    return route

def update_stop_status(route_id, stop_index, new_status):
    """
    Αλλάζει την κατάσταση μιας στάσης.
    new_status: 'done' ή 'skip'
    """
    from modules.database import load_data, save_data, ROUTES_FILE
    routes = load_data(ROUTES_FILE)
    for route in routes:
        if route["id"] == route_id:
            route["stops"][stop_index]["status"] = new_status
    save_data(ROUTES_FILE, routes)

def get_driver_routes(driver_username):
    """Επιστρέφει όλα τα routes ενός οδηγού."""
    all_routes = get_all_routes()
    return [r for r in all_routes if r["driver"] == driver_username]

def get_next_pending_stop(route):
    """Βρίσκει την επόμενη εκκρεμή στάση."""
    for i, stop in enumerate(route["stops"]):
        if stop["status"] == "pending":
            return i, stop
    return None, None

def show_driver_view(user):
    """
    Εμφανίζει την οθόνη του οδηγού.
    Ο οδηγός βλέπει τις στάσεις του και τις εκτελεί.
    """
    st.title("🚚 Οι Διαδρομές μου")
    
    routes = get_driver_routes(user["username"])
    
    if not routes:
        st.info("Δεν έχεις ακόμα διαδρομές.")
        return
    
    # Εμφάνιση τελευταίου route
    route = routes[-1]
    st.subheader(f"Διαδρομή {route['created_at']}")
    
    for i, stop in enumerate(route["stops"]):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        # Εικονίδιο κατάστασης
        if stop["status"] == "done":
            icon = "✅"
        elif stop["status"] == "skip":
            icon = "⏭️"
        else:
            icon = "🔴"
        
        col1.write(f"{icon} {i+1}. {stop['address']}")
        
        # Κουμπιά μόνο για pending στάσεις
        if stop["status"] == "pending":
            maps_url = get_google_maps_url(stop["address"])
            col1.markdown(f"[🗺️ Άνοιγμα στο Google Maps]({maps_url})")
            
            if col2.button("✅ Done", key=f"done_{i}"):
                update_stop_status(route["id"], i, "done")
                st.rerun()
            
            if col3.button("⏭️ Skip", key=f"skip_{i}"):
                update_stop_status(route["id"], i, "skip")
                st.rerun()
