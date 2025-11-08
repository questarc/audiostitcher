import streamlit as st

st.title("📁 Upload Audio Files")
st.markdown("Upload multiple audio files to begin stitching.")

uploaded_files = st.file_uploader("Choose audio files", type=["mp3", "wav", "ogg"], accept_multiple_files=True)

if uploaded_files:
    st.session_state["audio_files"] = uploaded_files
    st.success(f"{len(uploaded_files)} files uploaded successfully.")
