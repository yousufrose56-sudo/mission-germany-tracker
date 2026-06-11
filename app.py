import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import cloudinary.uploader

# --- PAGE CONFIG ---
st.set_page_config(page_title="Mission Germany CRM", layout="wide")

# --- LOGIN MECHANISM (ADD THIS) ---
# Create a sidebar for login
st.sidebar.title("Login")
user_email = st.sidebar.text_input("Enter your email")

# --- CONFIGURATIONS ---
# (Ensure your secrets are set up correctly in Streamlit Cloud)
cloudinary.config(
    cloud_name=st.secrets["cloudinary"]["cloud_name"],
    api_key=st.secrets["cloudinary"]["api_key"],
    api_secret=st.secrets["cloudinary"]["api_secret"]
)

# --- GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def get_sheet(tab_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = dict(st.secrets["gcp_service_account"])
    
    key = creds_dict["private_key"]
    formatted_key = "-----BEGIN PRIVATE KEY-----\n" + "\n".join([key[i:i+64] for i in range(0, len(key), 64)]) + "\n-----END PRIVATE KEY-----\n"
    creds_dict["private_key"] = formatted_key
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds) # FIX: You missed passing creds here
    
    # FIX: You need to open the workbook and then the specific sheet
    spreadsheet = client.open("Your_Google_Sheet_Name") 
    return spreadsheet.worksheet(tab_name)

# --- MAIN APP LOGIC ---
if user_email == "yousuf@gmail.com":
    # ... (rest of your admin dashboard logic)
elif user_email:
    # ... (rest of your user dashboard logic)
else:
    st.title("🇩🇪 Mission Germany CRM")
    st.write("Please log in via the sidebar to access the dashboard.")
