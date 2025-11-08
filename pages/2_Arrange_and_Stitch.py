import streamlit as st
from utils.audio_utils import stitch_audio

st.title("🧩 Arrange and Stitch")
st.markdown("Drag to reorder files and stitch them into one.")

audio_files = st.session_state.get("audio_files", [])

if not audio_files:
    st.warning("Please upload audio files first.")
else:
    order = st.multiselect("Select and order files", audio_files, default=audio_files)
    if st.button("Stitch Audio"):
        stitched_audio = stitch_audio(order)
        st.session_state["stitched_audio"] = stitched_audio
        st.success("Audio stitched successfully.")
