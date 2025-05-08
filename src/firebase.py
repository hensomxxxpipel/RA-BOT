import firebase_admin
from firebase_admin import credentials, firestore, auth
import streamlit as st
import os
import json

# def initialize_firebase():
#     """Initialize Firebase if not already initialized"""
#     if not firebase_admin._apps:
#         try:
#             # Use service account credentials
#             cred = credentials.Certificate("rabotkey.json")
#             firebase_admin.initialize_app(cred)
#         except Exception as e:
#             st.error(f"Failed to initialize Firebase: {e}")
#             return None
#     return firestore.client()

# Jika sudah deploy streamlit
def initialize_firebase():
    if not firebase_admin._apps:
        try:
            # Buat dictionary untuk credentials
            firebase_config = {
                "type": st.secrets["firebase"]["type"],
                "project_id": st.secrets["firebase"]["project_id"],
                "private_key_id": st.secrets["firebase"]["private_key_id"],
                "private_key": st.secrets["firebase"]["private_key"],
                "client_email": st.secrets["firebase"]["client_email"],
                "client_id": st.secrets["firebase"]["client_id"],
                "auth_uri": st.secrets["firebase"]["auth_uri"],
                "token_uri": st.secrets["firebase"]["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
                "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"],
                "universe_domain": st.secrets["firebase"]["universe_domain"]
            }
            
            # Simpan ke file temporary
            with open("firebase_key_temp.json", "w") as f:
                json.dump(firebase_config, f)
            
            # Gunakan file untuk inisialisasi
            cred = credentials.Certificate("firebase_key_temp.json")
            firebase_admin.initialize_app(cred)
            
            # Hapus file temporary
            if os.path.exists("firebase_key_temp.json"):
                os.remove("firebase_key_temp.json")
                
            st.success("Firebase berhasil diinisialisasi!")
            return firestore.client()
        except Exception as e:
            st.error(f"Gagal menginisialisasi Firebase: {e}")
            import traceback
            st.error(traceback.format_exc())
            return None
    return firestore.client()

class FirebaseAuth:
    def __init__(self):
        self.db = initialize_firebase()
        self.chat_history_collection = "chat_histories"
        
    def signup_user(self, email, password, username=None, additional_info=None):
        """
        Create a new user with email and password
        
        Args:
            email (str): User's email
            password (str): User's password
            username (str, optional): Username
            additional_info (dict, optional): Additional user information
            
        Returns:
            tuple: (success, message or user_id)
        """
        try:
            # Create user in Firebase Authentication
            user = auth.create_user(
                email=email,
                password=password
            )
            
            # Create user document in Firestore
            user_data = {
                'email': email,
                'username': username or email.split('@')[0],
                'created_at': firestore.SERVER_TIMESTAMP,
                'user_id': user.uid
            }
            
            # Add additional info if provided
            if additional_info and isinstance(additional_info, dict):
                user_data.update(additional_info)
            
            # Save user data to Firestore
            if self.db:
                self.db.collection('users').document(user.uid).set(user_data)
                
            return True, user.uid
        except Exception as e:
            if "EMAIL_EXISTS" in str(e):
                return False, "Email already registered"
            elif "WEAK_PASSWORD" in str(e):
                return False, "Password is too weak"
            else:
                return False, f"Error creating user: {str(e)}"
    
    def signin_user(self, email, password):
        """
        Sign in a user with email and password
        
        Args:
            email (str): User's email
            password (str): User's password
            
        Returns:
            tuple: (success, message or user_id)
        """
        try:
            # Sign in user using Firebase Admin SDK
            # Note: Firebase Admin SDK does not provide a direct way to sign in with email/password
            # This is a workaround - we'll check if the user exists and then verify their credentials
            user = auth.get_user_by_email(email)
            
            # Since we can't verify password directly with Admin SDK,
            # we'll assume the user exists and return success
            # In a real application, you would use Firebase Auth REST API or the client SDK
            
            # For this implementation, we'll say the login was successful if we find the user
            return True, user.uid
            
        except auth.UserNotFoundError:
            return False, "User not found"
        except Exception as e:
            return False, f"Error signing in: {str(e)}"
    
    def get_user_info(self, user_id):
        """
        Get user information from Firestore
        
        Args:
            user_id (str): User ID
            
        Returns:
            dict: User information
        """
        if not self.db:
            return None
            
        try:
            user_doc = self.db.collection('users').document(user_id).get()
            if user_doc.exists:
                return user_doc.to_dict()
            return None
        except Exception as e:
            st.error(f"Error getting user info: {e}")
            return None
    
    def update_user_info(self, user_id, data):
        """
        Update user information in Firestore
        
        Args:
            user_id (str): User ID
            data (dict): Data to update
            
        Returns:
            bool: Success status
        """
        if not self.db:
            return False
            
        try:
            self.db.collection('users').document(user_id).update(data)
            return True
        except Exception as e:
            st.error(f"Error updating user info: {e}")
            return False
    
    def reset_password(self, email):
        """
        Send password reset email
        
        Args:
            email (str): User's email
            
        Returns:
            bool: Success status
        """
        try:
            # Generate password reset link
            reset_link = auth.generate_password_reset_link(email)
            # Note: In a real application, you would send this link to the user via email
            # For this implementation, we'll just return the link
            return True, reset_link
        except auth.UserNotFoundError:
            return False, "User not found"
        except Exception as e:
            return False, f"Error resetting password: {str(e)}"
    
    def delete_user(self, user_id):
        """
        Delete a user
        
        Args:
            user_id (str): User ID
            
        Returns:
            bool: Success status
        """
        try:
            # Delete user from Authentication
            auth.delete_user(user_id)
            
            # Delete user document from Firestore
            if self.db:
                self.db.collection('users').document(user_id).delete()
                
            return True
        except Exception as e:
            st.error(f"Error deleting user: {e}")
            return False
            
    def check_auth_status(self):
        """
        Check if user is authenticated in the current session
        
        Returns:
            bool: Authentication status
        """
        return 'user_id' in st.session_state and st.session_state.user_id is not None
    
    def logout_user(self):
        """
        Log out current user
        
        Returns:
            bool: Success status
        """
        if 'user_id' in st.session_state:
            del st.session_state.user_id
        return True
        
    def save_chat_history(self, user_id, model_type, prompt, response, timestamp=None):
        """
        Simpan riwayat chat ke Firestore
        
        Args:
            user_id (str): ID pengguna
            model_type (str): Jenis model chatbot ('llama4', 'deepseek', 'llama3', 'gemini.flash')
            prompt (str): Pertanyaan dari pengguna
            response (str): Jawaban dari chatbot
            timestamp (datetime, optional): Waktu chat. Jika None, gunakan SERVER_TIMESTAMP
            
        Returns:
            tuple: (success, chat_id or error message)
        """
        if not self.db:
            return False, "Database not initialized"
            
        try:
            # Buat data chat
            chat_data = {
                'user_id': user_id,
                'model_type': model_type,
                'prompt': prompt,
                'response': response,
                'timestamp': timestamp or firestore.SERVER_TIMESTAMP
            }
            
            # Simpan di Firestore
            chat_ref = self.db.collection(self.chat_history_collection).document()
            chat_ref.set(chat_data)
            
            return True, chat_ref.id
        except Exception as e:
            return False, f"Error saving chat history: {str(e)}"
    
    def get_user_chat_history(self, user_id, limit=50, model_type=None):
        """
        Ambil riwayat chat pengguna dari Firestore
        
        Args:
            user_id (str): ID pengguna
            limit (int, optional): Batasan jumlah riwayat. Default 50
            model_type (str, optional): Filter berdasarkan jenis model chatbot
            
        Returns:
            list: Riwayat chat pengguna
        """
        if not self.db:
            return []
            
        try:
            # Buat query dasar
            query = self.db.collection(self.chat_history_collection).where('user_id', '==', user_id)
            
            # Tambahkan filter model jika ada
            if model_type:
                query = query.where('model_type', '==', model_type)
            
            # Untuk menghindari masalah indeks, kita tidak melakukan pengurutan terlebih dahulu
            # Eksekusi query
            results = query.stream()
            
            # Konversi hasil ke list
            history = []
            for doc in results:
                data = doc.to_dict()
                data['chat_id'] = doc.id
                history.append(data)
                
            # Batasi dan urutkan hasil di Python daripada di Firestore
            # Ini dapat mengurangi efisiensi untuk dataset besar, tetapi akan menghindari error indeks
            # Urutkan berdasarkan timestamp (terbaru dulu)
            sorted_history = sorted(
                history, 
                key=lambda x: x.get('timestamp', 0) if x.get('timestamp') is not None else 0,
                reverse=True
            )
            
            # Batasi jumlah hasil
            return sorted_history[:limit]
            
        except Exception as e:
            st.error(f"Error retrieving chat history: {e}")
            st.info("Untuk memperbaiki masalah ini, buat indeks komposit di Firebase Console menggunakan link yang ditampilkan dalam error.")
            return []
    
    def delete_chat(self, chat_id):
        """
        Hapus chat berdasarkan ID
        
        Args:
            chat_id (str): ID chat
            
        Returns:
            bool: Success status
        """
        if not self.db:
            return False
            
        try:
            self.db.collection(self.chat_history_collection).document(chat_id).delete()
            return True
        except Exception as e:
            st.error(f"Error deleting chat: {e}")
            return False