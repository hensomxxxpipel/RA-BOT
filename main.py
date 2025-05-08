# Update main.py
import streamlit as st
from src.login import login_page
from src.signup import signup_page
from src.app import app
from src.firebase import FirebaseAuth

st.set_page_config(page_title="RA-BOT", layout="wide")

# Inisialisasi session state
def init_session_state():
    defaults = {
        'users': {},
        'logged_in': False,
        'username': "",
        'page': 'login',
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Tambahkan fungsi untuk mengecek persistent session
def check_session():
    # Mengecek apakah ada token di cookie
    if 'token' in st.session_state and st.session_state.token:
        firebase_auth = FirebaseAuth()
        # Retrieve user data from the token
        user_id = st.session_state.token
        user_info = firebase_auth.get_user_info(user_id)
        
        if user_info:
            # Restore session
            st.session_state.user_id = user_id
            st.session_state.username = user_info.get('username', user_id)
            st.session_state.logged_in = True
            return True
    return False

# Routing berdasarkan status login dan halaman aktif
def main():
    # Cek apakah sudah login atau ada token
    if st.session_state.logged_in or check_session():
        app()
    else:
        page = st.session_state.page

        if page == 'login':
            login_page()
        elif page == 'signup':
            signup_page()
        else:
            # Default fallback jika page tidak dikenali
            st.session_state.page = 'login'
            login_page()

if __name__ == "__main__":
    main()