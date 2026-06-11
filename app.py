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
def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Convert secrets to dict and handle the newline character in the private key
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    # This opens the first tab of your Google Sheet
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
        st.write("Please ensure the Google Sheet 'Mission_Germany_CRM' is shared with your Service Account email.")

elif user_email:
    st.header(f"Welcome, {user_email}")
    st.write("Student dashboard access in progress.")
else:
    st.title("🇩🇪 Mission Germany CRM")
    st.write("Please log in via the sidebar.")
