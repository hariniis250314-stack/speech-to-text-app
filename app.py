import streamlit as st
import speech_recognition as sr
import tempfile

st.set_page_config(page_title="Speech to Text App", page_icon="🎙️")
st.title("🎙️ Speech-to-Text Transcription App")

st.markdown("Upload a `.wav` audio file (not mp3) to get the transcribed text.")

# Upload audio
audio_file = st.file_uploader("Upload .WAV Audio File", type=["wav"])

if audio_file:
    st.audio(audio_file, format="audio/wav")
    st.info("Processing audio...")

    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    # Use SpeechRecognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(tmp_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            st.success("Transcription Complete!")
            st.text_area("📝 Transcribed Text", text, height=300)

            # Download as .txt
            st.download_button(
                label="📥 Download Transcription",
                data=text,
                file_name="transcription.txt",
                mime="text/plain"
            )
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError:
            st.error("Could not connect to the Speech Recognition service.")
