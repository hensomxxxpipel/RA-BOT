import streamlit as st
from src.firebase import FirebaseAuth

def signup_page():
    firebase_auth = FirebaseAuth()

    st.markdown("""
        <div style="text-align: center;">
            <h2 style="color: rgb(255, 75, 75);">Buat Akun Baru RA-BOT ✨</h2>
            <p style="font-size: 16px;">Isi informasi di bawah ini untuk mendaftar.</p>
        </div>
    """, unsafe_allow_html=True)

    # Layout kolom agar form di tengah
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 📝 Daftar")
        new_email = st.text_input("📧 Email", key="signup_email", placeholder="contoh@email.com")
        new_username = st.text_input("👤 Username", key="signup_user", placeholder="Nama pengguna unik")
        new_password = st.text_input("🔑 Password", type="password", key="signup_pass", placeholder="Minimal 6 karakter")
        confirm_password = st.text_input("🔒 Konfirmasi Password", type="password", key="signup_conf", placeholder="Masukkan ulang password")

        st.markdown("---")

        if st.button("🚀 Daftar Sekarang", use_container_width=True):
            if not new_email or not new_username or not new_password:
                st.warning("Email, username, dan password harus diisi!")
            elif new_password != confirm_password:
                st.warning("Password tidak cocok!")
            elif "@" not in new_email or "." not in new_email:
                st.warning("Format email tidak valid!")
            else:
                additional_info = {
                    "username": new_username,
                    "display_name": new_username
                }

                success, message = firebase_auth.signup_user(
                    email=new_email,
                    password=new_password,
                    username=new_username,
                    additional_info=additional_info
                )

                if success:
                    st.session_state.user_id = message
                    st.session_state.username = new_username
                    st.session_state.logged_in = True
                    st.session_state.token = message
                    
                    st.success("Pendaftaran berhasil! 🎉")
                    st.session_state.page = 'app'
                    st.rerun()
                else:
                    st.error(f"Gagal mendaftar: {message}")

        if st.button("⬅️ Sudah punya akun? Login di sini", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()
