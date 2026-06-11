import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import cloudinary.uploader

st.set_page_config(page_title="Mission Germany CRM", layout="wide")

st.sidebar.title("Login")
user_email = st.sidebar.text_input("Enter your email")
user_password = st.sidebar.text_input("Enter your password", type="password")

cloudinary.config(
    cloud_name=st.secrets["cloudinary"]["cloud_name"],
    api_key=st.secrets["cloudinary"]["api_key"],
    api_secret=st.secrets["cloudinary"]["api_secret"]
)

@st.cache_resource
def get_sheet(tab_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = dict(st.secrets["gcp_service_account"])
    
    key = creds_dict["private_key"]
    formatted_key = "-----BEGIN PRIVATE KEY-----\n" + "\n".join([key[i:i+64] for i in range(0, len(key), 64)]) + "\n-----END PRIVATE KEY-----\n"
    creds_dict["private_key"] = formatted_key
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    spreadsheet = client.open("Mission_Germany_CRM") 
    return spreadsheet.worksheet(tab_name)

if user_email == "yousuf@gmail.com":
    st.header("Admin Dashboard: Manage Data")
    
    tab1, tab2 = st.tabs(["Students Data", "Team Data"])
    
    with tab1:
        try:
            st.subheader("Student Records")
            students_sheet = get_sheet("Students")
            students_data = students_sheet.get_all_records()
            st.dataframe(students_data, use_container_width=True) if students_data else st.write("No records.")
        except Exception as e:
            st.error(f"Error loading Students: {e}")

    with tab2:
        try:
            st.subheader("Team Records")
            team_sheet = get_sheet("Team")
            team_data = team_sheet.get_all_records()
            st.dataframe(team_data, use_container_width=True) if team_data else st.write("No records.")
        except Exception as e:
            st.error(f"Error loading Team: {e}")

elif user_email:
    st.header(f"Welcome, {user_email}")
    st.write("Student dashboard access is currently in development.")
else:
    st.title("🇩🇪 Mission Germany CRM")
    st.write("Please log in via the sidebar to access the dashboard.")
