import sys
import types

# Patch audioop using audioop-lts for Python 3.13+
try:
    import audioop_lts as audioop
    sys.modules['audioop'] = audioop
except ImportError:
    pass

import streamlit as st
from pydub import AudioSegment
import io

st.set_page_config(page_title="Audio Stitcher", page_icon="🎧", layout="centered")
st.title("🎧 Audio Stitcher")
st.markdown("Upload audio files (MP3, WAV, OGG, M4A), arrange them, stitch into one, and download.")

# Accept all files, filter manually
uploaded_files = st.file_uploader("📁 Upload audio files", type=None, accept_multiple_files=True)

# Filter supported extensions
supported_exts = (".mp3", ".wav", ".ogg", ".m4a")
audio_files = [f for f in uploaded_files if f.name.lower().endswith(supported_exts)]

if uploaded_files and not audio_files:
    st.error("Only MP3, WAV, OGG, and M4A files are supported.")

if audio_files:
    filenames = [file.name for file in audio_files]
    order = st.multiselect("🧩 Arrange files", filenames, default=filenames)
    ordered_files = [file for name in order for file in audio_files if file.name == name]

    if st.button("🔗 Stitch Audio"):
        final_audio = AudioSegment.empty()
        for file in ordered_files:
            try:
                audio = AudioSegment.from_file(file)
                final_audio += audio
            except Exception as e:
                st.error(f"Error processing {file.name}: {e}")

        buffer = io.BytesIO()
        final_audio.export(buffer, format="mp3")
        buffer.seek(0)
        st.session_state["stitched_audio"] = buffer
        st.success("✅ Audio stitched successfully!")

if "stitched_audio" in st.session_state:
    st.markdown("### ▶️ Preview")
    st.audio(st.session_state["stitched_audio"].read(), format="audio/mp3")
    st.session_state["stitched_audio"].seek(0)
    st.download_button("⬇️ Download Stitched Audio", st.session_state["stitched_audio"], file_name="stitched_output.mp3")
