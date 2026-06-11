import streamlit as st
import os

# Try to import google api libraries
try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseUpload
    from google.oauth2 import service_account
    import io
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False

st.set_page_config(page_title="Mission Germany", page_icon="🇩🇪", layout="wide")
st.title("🇩🇪 Mission Germany: Masters Application Tracker")
st.caption("Powered by TEN GERMANY | The Education Network")
st.markdown("---")

# Function to upload file to Google Drive
def upload_to_drive(file, filename):
    if not HAS_GOOGLE:
        st.error("Google libraries are missing. Please add them to requirements.txt")
        return None
    try:
        # Load credentials from Streamlit Secrets
        creds_dict = st.secrets["gcp_service_account"]
        
        # FIXED: Using your real email address to bypass the 0-byte quota wall
        user_to_impersonate = "yousufrose56@gmail.com" 
        
        creds = service_account.Credentials.from_service_account_info(
            creds_dict,
            scopes=["https://www.googleapis.com/auth/drive"],
            subject=user_to_impersonate
        )
        service = build('drive', 'v3', credentials=creds)
        
        # Define folder ID where files will save
        folder_id = st.secrets.get("google_drive_folder_id", None)
        
        file_metadata = {'name': filename}
        if folder_id:
            file_metadata['parents'] = [folder_id]
            
        media = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype='application/pdf', resumable=True)
        
        uploaded_file = service.files().create(
            body=file_metadata, 
            media_body=media, 
            fields='id',
            supportsAllDrives=True
        ).execute()
        
        return uploaded_file.get('id')
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return None

st.sidebar.header("🎓 Profile Evaluation")
cgpa = st.sidebar.number_input("Enter your CGPA (10-point scale):", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
st.sidebar.markdown("### Admission Probability")
if 5.0 <= cgpa < 7.5:
    st.sidebar.warning("🎯 **Private Universities:** High Probability\n\n*Public Universities may be highly competitive.*")
elif 7.5 <= cgpa < 8.0:
    st.sidebar.info("📈 **Public Universities:** ~60% Probability")
elif 8.0 <= cgpa < 8.5:
    st.sidebar.success("🚀 **Public Universities:** ~90% Probability")
elif 8.5 <= cgpa <= 10.0:
    st.sidebar.success("🏆 **Public Universities:** ~99% Probability (Excellent Profile)")

st.header("📍 Your Master's Journey Progress")
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["1. Assessment", "2. Pre-App", "3. Application", "4. Post-App", "5. Post-Acceptance", "6. Pre-Visa", "7. Post-Visa", "8. Post-Landing"])

with tab1:
    st.subheader("Stage 1: Assessment of Profile")
    st.checkbox("1. Recognition of University & Degree through Anabin")
    st.checkbox("2. CGPA Check")
    st.checkbox("3. Semester Mark sheets available")
    
    uploaded_marksheets = st.file_uploader("📤 Upload Semester Marksheets (PDF)", type=["pdf"], accept_multiple_files=True, key="marksheets")
    if uploaded_marksheets:
        for f in uploaded_marksheets:
            if st.button(f"Save {f.name} to Drive"):
                with st.spinner("Uploading..."):
                    file_id = upload_to_drive(f, f.name)
                    if file_id:
                        st.success(f"🎉 Successfully saved {f.name} to Google Drive!")
    
    st.checkbox("4. Degree Certificate / Provisional available")
    uploaded_degree = st.file_uploader("📤 Upload Degree Certificate / Provisional (PDF)", type=["pdf"], key="degree")
    if uploaded_degree:
        if st.button("Save Degree Certificate to Drive"):
            with st.spinner("Uploading..."):
                file_id = upload_to_drive(uploaded_degree, uploaded_degree.name)
                if file_id:
                    st.success("🎉 Successfully saved Degree to Google Drive!")
    
    st.checkbox("5. Passport Validity verified & Aadhar mobile linked")
    uploaded_passport = st.file_uploader("📤 Upload Passport Copy (PDF/Image)", type=["pdf", "png", "jpg"], key="passport")
    if uploaded_passport:
        if st.button("Save Passport to Drive"):
            with st.spinner("Uploading..."):
                file_id = upload_to_drive(uploaded_passport, uploaded_passport.name)
                if file_id:
                    st.success("🎉 Successfully saved Passport to Google Drive!")

with tab2: st.subheader("Stage 2: Pre-Application Steps"); st.checkbox("1. Online APS Application submitted & Documents couriered"); st.checkbox("2. Letters of Recommendation (LORs) secured & Europass CV prepared"); st.checkbox("3. English Proficiency Test written (IELTS/TOEFL)"); st.checkbox("4. Final University Short-listing completed"); st.checkbox("5. Preparation of Course-specific LOM / SOP")
with tab3: st.subheader("Stage 3: Submitting Applications"); app_method = st.radio("Select pathway:", ("Direct Portal", "Uni-Assist", "VPD through Uni-Assist")); st.checkbox("1. Registration on respective portal complete"); st.checkbox("2. Documents uploaded / couriered"); st.checkbox("3. Application fee paid & submitted")
with tab4: st.subheader("Stage 4: Post-Application Phase"); st.checkbox("1. Follow-ups maintained"); st.checkbox("2. Attended Tests/Interviews"); st.checkbox("3. German Visa Slot booked")
with tab5: st.subheader("Stage 5: Post-Acceptance / Enrolment"); st.checkbox("1. Complete Enrolment Process"); st.checkbox("2. Purchase Student Health Insurance"); st.checkbox("3. Payment of Semester Contribution")
with tab6: st.subheader("Stage 6: Pre-Visa Interview Preparation"); st.checkbox("1. Accumulate German National Visa Docs"); st.checkbox("2. Open German Blocked Account"); st.checkbox("3. Prepare Visa LOM & Cover Letter")
with tab7: st.subheader("Stage 7: Post-Visa Approval (Pre-Departure)"); st.checkbox("1. Flight Ticket Booked"); st.checkbox("2. Temporary Accommodation arranged"); st.checkbox("3. German SIM Card ordered")
with tab8: st.subheader("Stage 8: Post-Landing Formalities"); st.checkbox("1. Sign Rental Contract"); st.checkbox("2. Complete City Registration (Anmeldung)"); st.checkbox("3. Unblock Blocked Account")
