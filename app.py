import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import cloudinary.uploader

# --- GOOGLE SHEETS CONFIG ---
def get_sheet_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    return client.open("Mission_Germany_CRM").sheet1

# --- LOGIN LOGIC ---
st.set_page_config(page_title="Mission Germany CRM", layout="wide")
st.sidebar.title("Login")
user_email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

# Admin login check
if user_email == "yousuf@gmail.com":
    st.header("Admin Dashboard: Manage Students")
    try:
        sheet = get_sheet_data()
        data = sheet.get_all_records()
        # Using dataframe allows sorting and better visualization for 50+ students
        st.dataframe(data, use_container_width=True) 
    except Exception as e:
        st.error(f"Could not load Google Sheet: {e}")
else:
    st.header("Student Dashboard")
    st.write("Welcome! Please log in to see your personalized tracker.")

# --- CLOUDINARY LOGIC ---
cloudinary.config(
    cloud_name = st.secrets["cloudinary"]["cloud_name"],
    api_key = st.secrets["cloudinary"]["api_key"],
    api_secret = st.secrets["cloudinary"]["api_secret"]
)
