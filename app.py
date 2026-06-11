import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import cloudinary.uploader

# --- PAGE CONFIG ---
st.set_page_config(page_title="Mission Germany CRM", layout="wide")

# --- CONFIGURATIONS ---
cloudinary.config(
    cloud_name=st.secrets["cloudinary"]["cloud_name"],
    api_key=st.secrets["cloudinary"]["api_key"],
    api_secret=st.secrets["cloudinary"]["api_secret"]
)

# --- GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def get_sheet(tab_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Get credentials from secrets and handle the private key newline formatting
    secrets_dict = dict(st.secrets["gcp_service_account"])
    secrets_dict["private_key"] = secrets_dict["private_key"].replace("\\n", "\n")
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(secrets_dict, scope)
    client = gspread.authorize(creds)
    
    # Opens the specific tab by name
    return client.open("Mission_Germany_CRM").worksheet(tab_name)

# --- LOGIN LOGIC ---
st.sidebar.title("Login")
user_email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

# --- MAIN APP LOGIC ---
if user_email == "yousuf@gmail.com":
    st.header("Admin Dashboard: Manage Students")
    try:
        # Access the "Students" tab specifically
        sheet = get_sheet("Students")
        data = sheet.get_all_records()
        if data:
            st.dataframe(data, use_container_width=True)
        else:
            st.write("No student records found in the 'Students' tab.")
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        st.write("Ensure your Google Sheet is named 'Mission_Germany_CRM' and has a tab named 'Students'.")
        st.write("Also, ensure the service account email is added as an 'Editor' on the Google Sheet.")

elif user_email:
    st.header(f"Welcome, {user_email}")
    st.write("Student dashboard access is currently in development.")
else:
    st.title("🇩🇪 Mission Germany CRM")
    st.write("Please log in via the sidebar to access the dashboard.")
