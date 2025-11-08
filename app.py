import streamlit as st
import ffmpeg
import tempfile
import os
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
        with tempfile.TemporaryDirectory() as tmpdir:
            input_paths = []
            for file in ordered_files:
                path = os.path.join(tmpdir, file.name)
                with open(path, "wb") as f:
                    f.write(file.read())
                input_paths.append(path)

            try:
                # Build input streams
                inputs = [ffmpeg.input(p) for p in input_paths]
                joined = ffmpeg.concat(*inputs, v=0, a=1).output('pipe:', format='mp3')

                out, _ = joined.run(capture_stdout=True, capture_stderr=True)
                stitched = io.BytesIO(out)
                st.session_state["stitched_audio"] = stitched
                st.success("✅ Audio stitched successfully!")
            except ffmpeg.Error as e:
                st.error("FFmpeg error during stitching.")
                st.text(e.stderr.decode())

if "stitched_audio" in st.session_state:
    st.markdown("### ▶️ Preview")
    st.audio(st.session_state["stitched_audio"].read(), format="audio/mp3")
    st.session_state["stitched_audio"].seek(0)
    st.download_button("⬇️ Download Stitched Audio", st.session_state["stitched_audio"], file_name="stitched_output.mp3")
