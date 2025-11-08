import streamlit as st
import ffmpeg
import tempfile
import os
import io

st.set_page_config(page_title="Audio Stitcher", page_icon="🎧", layout="centered")
st.title("🎧 Audio Stitcher")
st.markdown("Upload audio files (MP3, WAV, OGG), arrange them, stitch into one, and download.")

uploaded_files = st.file_uploader("📁 Upload audio files", type=["mp3", "wav", "ogg"], accept_multiple_files=True)

if uploaded_files:
    filenames = [file.name for file in uploaded_files]
    order = st.multiselect("🧩 Arrange files", filenames, default=filenames)
    ordered_files = [file for name in order for file in uploaded_files if file.name == name]

    if st.button("🔗 Stitch Audio"):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_paths = []
            for i, file in enumerate(ordered_files):
                path = os.path.join(tmpdir, f"input_{i}.mp3")
                with open(path, "wb") as f:
                    f.write(file.read())
                input_paths.append(path)

            # Build ffmpeg input streams
            inputs = [ffmpeg.input(p) for p in input_paths]
            joined = ffmpeg.concat(*inputs, v=0, a=1).output('pipe:', format='mp3')

            try:
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
