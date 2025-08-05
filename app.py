mport streamlit as st
import speech_recognition as sr
import tempfile
from pydub import AudioSegment

st.set_page_config(page_title="Speech to Text App", page_icon="🎙️")
st.title("🎙️ Speech-to-Text Transcription App")

st.markdown("Upload an audio file (.mp3 or .wav) and get the transcribed text.")

# File uploader
audio_file = st.file_uploader("Upload Audio File", type=["mp3", "wav"])

if audio_file is not None:
    st.audio(audio_file, format='audio/wav')
    st.info("Processing audio...")

    # Save audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        if audio_file.type == "audio/mp3":
            audio = AudioSegment.from_file(audio_file, format="mp3")
        else:
            audio = AudioSegment.from_file(audio_file, format="wav")
        audio.export(tmp_file.name, format="wav")

        # Transcribe
        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_file.name) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                st.success("Transcription Complete!")
                st.text_area("📝 Transcribed Text", text, height=300)

                # Download button
                st.download_button(
                    label="📥 Download Transcription",
                    data=text,
                    file_name="transcription.txt",
                    mime="text/plain"
                )

            except sr.UnknownValueError:
                st.error("Speech Recognition could not understand the audio.")
            except sr.RequestError:
                st.error("Could not connect to the speech recognition service.")
