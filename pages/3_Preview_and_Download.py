import streamlit as st

st.title("▶️ Preview and Download")
st.markdown("Listen to the stitched audio and download it.")

stitched_audio = st.session_state.get("stitched_audio", None)

if stitched_audio:
    st.audio(stitched_audio.read(), format="audio/mp3")
    st.download_button("Download Stitched Audio", stitched_audio, file_name="stitched_output.mp3")
else:
    st.warning("No stitched audio found. Please complete the previous steps.")
