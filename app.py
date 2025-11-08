import streamlit as st
import wave
import audioop
import io

st.set_page_config(page_title="WAV Stitcher", page_icon="🎧", layout="centered")
st.title("🎧 WAV Stitcher")
st.markdown("""
Upload multiple WAV files, arrange them in order, stitch them into one, and download the result.
""")

# Step 1: Upload
uploaded_files = st.file_uploader("📁 Upload WAV files", type=["wav"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded.")

    # Step 2: Arrange
    filenames = [file.name for file in uploaded_files]
    order = st.multiselect("🧩 Select and order files", filenames, default=filenames)

    ordered_files = [file for name in order for file in uploaded_files if file.name == name]

    # Step 3: Stitch
    if st.button("🔗 Stitch WAV"):
        output_buffer = io.BytesIO()
        output_wave = None

        for file in ordered_files:
            with wave.open(file, 'rb') as wav:
                params = wav.getparams()
                frames = wav.readframes(wav.getnframes())

                if output_wave is None:
                    output_wave = wave.open(output_buffer, 'wb')
                    output_wave.setparams(params)
                else:
                    # Ensure same format
                    if wav.getparams() != output_wave.getparams():
                        st.error(f"Format mismatch in {file.name}. All files must have same sample rate, channels, and width.")
                        output_wave.close()
                        output_buffer.close()
                        output_wave = None
                        break

                output_wave.writeframes(frames)

        if output_wave:
            output_wave.close()
            output_buffer.seek(0)
            st.session_state["stitched_wav"] = output_buffer
            st.success("✅ WAV stitched successfully!")

# Step 4: Preview & Download
stitched_wav = st.session_state.get("stitched_wav", None)
if stitched_wav:
    st.markdown("### ▶️ Preview")
    st.audio(stitched_wav.read(), format="audio/wav")
    stitched_wav.seek(0)
    st.download_button("⬇️ Download Stitched WAV", stitched_wav, file_name="stitched_output.wav")
