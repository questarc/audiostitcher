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
                path = os.path.join(tmpdir, f"input_{i}")
                with open(path, "wb") as f:
                    f.write(file.read())
                input_paths.append(path)

            concat_list_path = os.path.join(tmpdir, "concat.txt")
            with open(concat_list_path, "w") as f:
                for path in input_paths:
                    f.write(f"file '{path}'\n")

            output_path = os.path.join(tmpdir, "output.mp3")
            try:
                ffmpeg.input(concat_list_path, format='concat', safe=0).output(output_path, acodec='libmp3lame').run(overwrite_output=True)
                with open(output_path, "rb") as f:
                    stitched = io.BytesIO(f.read())
                    st.session_state["stitched_audio"] = stitched
                    st.success("✅ Audio stitched successfully!")
            except ffmpeg.Error as e:
                st.error(f"FFmpeg error: {e.stderr.decode()}")

if "stitched_audio" in st.session_state:
    st.markdown("### ▶️ Preview")
    st.audio(st.session_state["stitched_audio"].read(), format="audio/mp3")
    st.session_state["stitched_audio"].seek(0)
    st.download_button("⬇️ Download Stitched Audio", st.session_state["stitched_audio"], file_name="stitched_output.mp3")
