import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import cloudinary.uploader

# 1. Setup Google Sheets Connection
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# You need to add your service account JSON to Streamlit Secrets as "gcp_service_account"
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)
sheet = client.open("Mission_Germany_CRM").sheet1

# 2. Basic Login (Admin: yousuf@gmail.com)
st.sidebar.title("Login")
user_email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if user_email == "yousuf@gmail.com": # Admin Logic
    st.header("Admin Dashboard: Manage Students")
    data = sheet.get_all_records()
    st.table(data)
else:
    st.header("Student Dashboard")
    # Student specific logic: filter sheet for their email
    st.write("Welcome to your personal tracker.")

# (Include your previous Cloudinary logic here to handle uploads)
