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
    creds_dict = dict(st.secrets["gcp_service_account"])
    raw_key = creds_dict["private_key"].strip()
    # Correct key formatting
    formatted_key = "-----BEGIN PRIVATE KEY-----\n" + "\n".join([raw_key[i:i+64] for i in range(0, len(raw_key), 64)]) + "\n-----END PRIVATE KEY-----\n"
    creds_dict["private_key"] = formatted_key
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open("Mission_Germany_CRM").worksheet(tab_name)

# --- LOGIN LOGIC ---
st.sidebar.title("Login")
user_email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

# --- MAIN APP LOGIC ---
if user_email:
    if user_email == "yousuf@gmail.com":
        st.header("Admin Dashboard: Manage Data")
        tab1, tab2 = st.tabs(["Students Data", "Team Data"])
        with tab1:
            try:
                st.subheader("Student Records")
                students_sheet = get_sheet("Students")
                st.dataframe(students_sheet.get_all_records(), use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")
        with tab2:
            try:
                st.subheader("Team Records")
                team_sheet = get_sheet("Team")
                st.dataframe(team_sheet.get_all_records(), use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")
    
    else:
        # STUDENT DASHBOARD
        st.header(f"Welcome, {user_email}")
        st.write("Upload your documents here:")
        
        # --- THE UPLOADER YOU WERE LOOKING FOR ---
        uploaded_file = st.file_uploader("Choose a document", type=["pdf", "png", "jpg"])
        if uploaded_file is not None:
            st.success(f"File {uploaded_file.name} ready for processing.")
            # Add your Cloudinary/processing logic here
            
else:
    st.title("🇩🇪 Mission Germany CRM")
    st.write("Please log in via the sidebar to access the dashboard.")
