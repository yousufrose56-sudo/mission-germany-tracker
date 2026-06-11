import streamlit as st
import os

try:
    import cloudinary
    import cloudinary.uploader
    HAS_CLOUDINARY = True
except ImportError:
    HAS_CLOUDINARY = False

st.set_page_config(page_title="Mission Germany", page_icon="🇩🇪", layout="wide")
st.title("🇩🇪 Mission Germany: Masters Application Tracker")
st.caption("Powered by TEN GERMANY | The Education Network")
st.markdown("---")

# Configure Cloudinary Integration
if HAS_CLOUDINARY:
    try:
        cloudinary.config(
            cloud_name = st.secrets["cloudinary"]["cloud_name"],
            api_key = st.secrets["cloudinary"]["api_key"],
            api_secret = st.secrets["cloudinary"]["api_secret"],
            secure = True
        )
    except Exception:
        HAS_CLOUDINARY = False

# High-performance upload function
def upload_file_to_storage(file, filename):
    if not HAS_CLOUDINARY:
        st.error("Storage configuration is finalizing. Please refresh the page.")
        return None
    try:
        response = cloudinary.uploader.upload(
            file,
            public_id = filename.split('.')[0],
            resource_type = "auto"
        )
        return response.get("secure_url")
    except Exception as e:
        st.error(f"Storage Upload Failed: {e}")
        return None

st.sidebar.header("🎓 Profile Evaluation")
cgpa = st.sidebar.number_input("Enter your CGPA (10-point scale):", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
st.sidebar.markdown("### Admission Probability")
if 5.0 <= cgpa < 7.5:
    st.sidebar.warning("🎯 **Private Universities:** High Probability")
elif 7.5 <= cgpa < 8.0:
    st.sidebar.info("📈 **Public Universities:** ~60% Probability")
elif 8.0 <= cgpa < 8.5:
    st.sidebar.success("🚀 **Public Universities:** ~90% Probability")
elif 8.5 <= cgpa <= 10.0:
    st.sidebar.success("🏆 **Public Universities:** ~99% Probability")

st.header("📍 Your Master's Journey Progress")
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["1. Assessment", "2. Pre-App", "3. Application", "4. Post-App", "5. Post-Acceptance", "6. Pre-Visa", "7. Post-Visa", "8. Post-Landing"])

with tab1:
    st.subheader("Stage 1: Assessment of Profile")
    
    # Marksheets Upload
    uploaded_marksheets = st.file_uploader("📤 Upload Semester Marksheets (PDF)", type=["pdf"], accept_multiple_files=True, key="marksheets")
    if uploaded_marksheets:
        for f in uploaded_marksheets:
            if st.button(f"Save {f.name} to Cloud"):
                with st.spinner("Uploading..."):
                    url = upload_file_to_storage(f, f.name)
                    if url:
                        st.success(f"🎉 Saved {f.name}!")
                        st.markdown(f'<a href="{url}" target="_blank">🔗 Click here to view/download {f.name}</a>', unsafe_allow_html=True)
    
    # Degree Upload
    uploaded_degree = st.file_uploader("📤 Upload Degree Certificate (PDF)", type=["pdf"], key="degree")
    if uploaded_degree:
        if st.button("Save Degree Certificate to Cloud"):
            with st.spinner("Uploading..."):
                url = upload_file_to_storage(uploaded_degree, uploaded_degree.name)
                if url:
                    st.success("🎉 Saved Degree!")
                    st.markdown(f'<a href="{url}" target="_blank">🔗 Click here to view/download Degree</a>', unsafe_allow_html=True)
    
    # Passport Upload
    uploaded_passport = st.file_uploader("📤 Upload Passport Copy (PDF/Image)", type=["pdf", "png", "jpg"], key="passport")
    if uploaded_passport:
        if st.button("Save Passport to Cloud"):
            with st.spinner("Uploading..."):
                url = upload_file_to_storage(uploaded_passport, uploaded_passport.name)
                if url:
                    st.success("🎉 Saved Passport!")
                    st.markdown(f'<a href="{url}" target="_blank">🔗 Click here to view/download Passport</a>', unsafe_allow_html=True)

with tab2: st.subheader("Stage 2: Pre-Application"); st.checkbox("1. APS Application"); st.checkbox("2. LORs & CV"); st.checkbox("3. English Tests"); st.checkbox("4. Shortlisting"); st.checkbox("5. SOP/LOM Preparation")
with tab3: st.subheader("Stage 3: Applications"); st.radio("Pathway:", ("Direct", "Uni-Assist", "VPD")); st.checkbox("1. Registered"); st.checkbox("2. Documents uploaded"); st.checkbox("3. Fee paid")
with tab4: st.subheader("Stage 4: Post-Application"); st.checkbox("1. Follow-ups"); st.checkbox("2. Interviews"); st.checkbox("3. Visa Slot booked")
with tab5: st.subheader("Stage 5: Post-Acceptance"); st.checkbox("1. Enrolment"); st.checkbox("2. Insurance"); st.checkbox("3. Fee payment")
with tab6: st.subheader("Stage 6: Visa Prep"); st.checkbox("1. Docs ready"); st.checkbox("2. Blocked Account"); st.checkbox("3. Visa LOM")
with tab7: st.subheader("Stage 7: Pre-Departure"); st.checkbox("1. Flight booked"); st.checkbox("2. Accommodation"); st.checkbox("3. SIM card")
with tab8: st.subheader("Stage 8: Post-Landing"); st.checkbox("1. Rental contract"); st.checkbox("2. Anmeldung"); st.checkbox("3. Unblock Account")
