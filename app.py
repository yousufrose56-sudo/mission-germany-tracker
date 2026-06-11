import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import cloudinary.uploader

# --- PAGE CONFIG ---
st.set_page_config(page_title="Mission Germany CRM", layout="wide")

# --- GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Using the credentials from your correctly formatted Secrets
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    return client.open("Mission_Germany_CRM").sheet1

# --- LOGIN LOGIC ---
st.sidebar.title("Login")
user_email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

# --- MAIN APP LOGIC ---
if user_email == "yousuf@gmail.com":
    st.header("Admin Dashboard: Manage Students")
    try:
        sheet = get_sheet()
        data = sheet.get_all_records()
        if data:
            st.dataframe(data, use_container_width=True)
        else:
            st.write("No student records found in the sheet.")
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        st.info("Check if your service account email has 'Editor' access to the Google Sheet.")

elif user_email: # Basic placeholder for student login
    st.header(f"Welcome, {user_email}")
    st.write("Student dashboard coming soon.")
else:
    st.title("🇩🇪 Mission Germany CRM")
    st.write("Please log in via the sidebar.")

# --- CLOUDINARY CONFIG ---
cloudinary.config(
    cloud_name = st.secrets["cloudinary"]["cloud_name"],
    api_key = st.secrets["cloudinary"]["api_key"],
    api_secret = st.secrets["cloudinary"]["api_secret"]
)
