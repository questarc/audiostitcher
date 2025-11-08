import streamlit as st
from pydub import AudioSegment
import io

st.set_page_config(page_title="Audio Stitcher Pro", page_icon="🎧", layout="centered")

st.title("🎧 Audio Stitcher Pro")
st.markdown("""
Upload multiple audio files (MP3, WAV, OGG), arrange them in your desired order, stitch them into one, and download the final result.
""")

# Step 1: Upload
uploaded_files = st.file_uploader("📁 Upload audio files", type=["mp3", "wav", "ogg"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded.")
    
    # Step 2: Arrange
    st.markdown("### 🧩 Arrange Order")
    filenames = [file.name for file in uploaded_files]
    order = st.multiselect("Select and order files", filenames, default=filenames)

    # Map selected filenames back to uploaded files
    ordered_files = [file for name in order for file in uploaded_files if file.name == name]

    # Step 3: Stitch
    if st.button("🔗 Stitch Audio"):
        final_audio = AudioSegment.empty()
        for file in ordered_files:
            try:
                audio = AudioSegment.from_file(file)
                final_audio += audio
            except Exception as e:
                st.error(f"Error processing {file.name}: {e}")

        # Export to buffer
        buffer = io.BytesIO()
        final_audio.export(buffer, format="mp3")
        buffer.seek(0)
        st.session_state["stitched_audio"] = buffer
        st.success("✅ Audio stitched successfully!")

# Step 4: Preview & Download
stitched_audio = st.session_state.get("stitched_audio", None)
if stitched_audio:
    st.markdown("### ▶️ Preview")
    st.audio(stitched_audio.read(), format="audio/mp3")
    stitched_audio.seek(0)
    st.download_button("⬇️ Download Stitched Audio", stitched_audio, file_name="stitched_output.mp3")
