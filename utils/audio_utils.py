from pydub import AudioSegment
import io

def stitch_audio(files):
    final_audio = AudioSegment.empty()
    for file in files:
        audio = AudioSegment.from_file(file)
        final_audio += audio
    buffer = io.BytesIO()
    final_audio.export(buffer, format="mp3")
    buffer.seek(0)
    return buffer
