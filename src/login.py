import streamlit as st
from src.firebase import FirebaseAuth

def login_page():
    firebase_auth = FirebaseAuth()
    
    st.markdown("""
        <div style="text-align: center;">
            <h2 style="color: rgb(255, 75, 75);">Selamat Datang Kembali di RA-BOT 👋</h2>
            <p style="font-size: 16px;">Silakan masuk ke akun Anda untuk melanjutkan.</p>
        </div>
    """, unsafe_allow_html=True)

    # Kolom layout agar lebih estetis
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Login")
        email = st.text_input("📧 Email", key="login_email", placeholder="contoh@email.com")
        password = st.text_input("🔑 Password", type="password", key="login_pass", placeholder="Minimal 6 karakter")

        st.markdown("---")

    # Kolom untuk memusatkan tombol login dan lupa password
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Login", use_container_width=True):
                if not email or not password:
                    st.warning("Email dan password harus diisi!")
                else:
                    success, user_id = firebase_auth.signin_user(email, password)
                    if success:
                        st.session_state.user_id = user_id
                        st.session_state.logged_in = True
                        st.session_state.token = user_id
                        
                        user_info = firebase_auth.get_user_info(user_id)
                        if user_info and 'username' in user_info:
                            st.session_state.username = user_info['username']
                        else:
                            st.session_state.username = email.split('@')[0]

                        st.success("Login berhasil! 🔓")
                        st.session_state.page = 'app'
                        st.rerun()
                    else:
                        st.error("Email atau password salah 😕")

        with col2:
            if st.button("🔁 Lupa Password?", use_container_width=True):
                if not email:
                    st.warning("Masukkan email Anda terlebih dahulu.")
                else:
                    success, message = firebase_auth.reset_password(email)
                    if success:
                        st.success("Email reset password telah dikirim 📩")
                    else:
                        st.error(f"Gagal mengirim email reset: {message}")

        # Tombol Daftar di bawahnya
        if st.button("📝 Belum punya akun? Daftar di sini", use_container_width=True):
            st.session_state.page = 'signup'
            st.rerun()