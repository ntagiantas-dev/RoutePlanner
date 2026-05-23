# ============================================
# APP.PY - ΚΕΝΤΡΙΚΟ ΑΡΧΕΙΟ
# Εδώ ξεκινάει η εφαρμογή
# Ελέγχει το login και κατευθύνει τον χρήστη
# στη σωστή οθόνη (οδηγός ή dispatcher)
# ============================================

import streamlit as st
from modules.database import init_database
from modules.auth import login, logout, create_default_users
from modules.routes import show_driver_view

# Αρχικοποίηση βάσης δεδομένων
init_database()

# Δημιουργία δοκιμαστικών χρηστών αν δεν υπάρχουν
create_default_users()

# Αρχικοποίηση session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

# ============================================
# ΚΥΡΙΟ MENU
# ============================================

if not st.session_state.logged_in:
    # Εμφάνισε login αν δεν είναι συνδεδεμένος
    login()
else:
    user = st.session_state.user
    role = user["role"]

    # Κουμπί αποσύνδεσης
    if st.sidebar.button("🚪 Αποσύνδεση"):
        logout()
        st.rerun()

    st.sidebar.write(f"👤 {user['username']}")
    st.sidebar.write(f"🎭 {role}")

    # Κατεύθυνση ανάλογα με τον ρόλο
    if role == "driver":
        # Οδηγός βλέπει τις διαδρομές του
        show_driver_view(user)

    elif role == "dispatcher":
        # Dispatcher βλέπει όλους τους οδηγούς
        st.title("📊 Dashboard Dispatcher")
        st.info("Σύντομα: Live παρακολούθηση οδηγών!")

        from modules.database import get_all_routes
        routes = get_all_routes()

        if not routes:
            st.warning("Δεν υπάρχουν ακόμα διαδρομές.")
        else:
            for route in routes:
                st.subheader(f"🚚 Οδηγός: {route['driver']}")
                for i, stop in enumerate(route["stops"]):
                    if stop["status"] == "done":
                        icon = "✅"
                    elif stop["status"] == "skip":
                        icon = "⏭️"
                    else:
                        icon = "🔴"
                    st.write(f"{icon} {i+1}. {stop['address']}")
