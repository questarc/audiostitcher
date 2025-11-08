import streamlit as st

st.set_page_config(page_title="Audio Stitcher Pro", page_icon="🎧", layout="wide")

st.sidebar.title("Audio Stitcher Pro")
st.sidebar.markdown("Navigate through the pages to upload, arrange, stitch, and download your audio files.")

st.title("Welcome to Audio Stitcher Pro 🎶")
st.markdown("""
This app lets you:
- Upload multiple audio files (MP3, WAV, OGG)
- Arrange them in your desired order
- Stitch them into a single audio file
- Preview and download the final result
""")
