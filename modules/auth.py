# ============================================
# AUTH MODULE
# Υπεύθυνο για login και διαχείριση χρηστών
# Roles: 'driver' (οδηγός) και 'dispatcher' (διαχειριστής)
# ============================================

import streamlit as st
from modules.database import get_all_users, save_user
import hashlib

def hash_password(password):
    """Κρυπτογραφεί τον κωδικό για ασφάλεια."""
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    """
    Εμφανίζει τη φόρμα login.
    Επιστρέφει True αν ο χρήστης συνδέθηκε επιτυχώς.
    """
    st.title("🚚 Route Planner")
    st.subheader("Σύνδεση")

    username = st.text_input("Όνομα χρήστη")
    password = st.text_input("Κωδικός", type="password")

    if st.button("Σύνδεση"):
        users = get_all_users()
        hashed = hash_password(password)
        for user in users:
            if user["username"] == username and user["password"] == hashed:
                # Αποθήκευσε τον χρήστη στο session
                st.session_state.user = user
                st.session_state.logged_in = True
                return True
        st.error("Λάθος όνομα χρήστη ή κωδικός!")
    return False

def logout():
    """Αποσύνδεση χρήστη - καθαρίζει το session."""
    st.session_state.user = None
    st.session_state.logged_in = False

def create_default_users():
    """
    Δημιουργεί δοκιμαστικούς χρήστες αν δεν υπάρχουν.
    Driver: username=driver1, password=1234
    Dispatcher: username=dispatcher1, password=1234
    """
    users = get_all_users()
    if len(users) == 0:
        save_user({"username": "driver1", "password": hash_password("1234"), "role": "driver"})
        save_user({"username": "dispatcher1", "password": hash_password("1234"), "role": "dispatcher"})
