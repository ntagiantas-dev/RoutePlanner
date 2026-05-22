# ============================================
# DATABASE MODULE
# Υπεύθυνο για την αποθήκευση & ανάκτηση δεδομένων
# Χρησιμοποιούμε απλά JSON αρχεία για το MVP
# Αργότερα μπορούμε να το αλλάξουμε σε PostgreSQL
# ============================================

import json
import os

# Τα αρχεία που αποθηκεύουμε τα δεδομένα
ROUTES_FILE = "data/routes.json"
USERS_FILE = "data/users.json"

def init_database():
    """
    Δημιουργεί τους φακέλους και αρχεία αν δεν υπάρχουν.
    Τρέχει μία φορά όταν ξεκινά η εφαρμογή.
    """
    # Δημιούργησε τον φάκελο data αν δεν υπάρχει
    os.makedirs("data", exist_ok=True)
    
    # Αν δεν υπάρχει το αρχείο routes, φτιάξε το κενό
    if not os.path.exists(ROUTES_FILE):
        save_data(ROUTES_FILE, [])
    
    # Αν δεν υπάρχει το αρχείο users, φτιάξε το κενό
    if not os.path.exists(USERS_FILE):
        save_data(USERS_FILE, [])

def save_data(filepath, data):
    """
    Αποθηκεύει δεδομένα σε JSON αρχείο.
    filepath: το μονοπάτι του αρχείου
    data: τα δεδομένα (λίστα ή dictionary)
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_data(filepath):
    """
    Φορτώνει δεδομένα από JSON αρχείο.
    Επιστρέφει κενή λίστα αν το αρχείο δεν υπάρχει.
    """
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def get_all_routes():
    """Επιστρέφει όλα τα routes από το αρχείο."""
    return load_data(ROUTES_FILE)

def save_route(route):
    """
    Αποθηκεύει ένα νέο route.
    route: dictionary με τα στοιχεία του route
    """
    routes = get_all_routes()
    routes.append(route)
    save_data(ROUTES_FILE, routes)

def get_all_users():
    """Επιστρέφει όλους τους χρήστες."""
    return load_data(USERS_FILE)

def save_user(user):
    """
    Αποθηκεύει έναν νέο χρήστη.
    user: dictionary με τα στοιχεία του χρήστη
    """
    users = get_all_users()
    users.append(user)
    save_data(USERS_FILE, users)
