import speech_recognition as sr
from pydub import AudioSegment  # Add this import statement

# Initialize the recognizer
recognizer = sr.Recognizer()

# Load the WAV file
audio_file =  "/home/alicode/Desktop/audio data/WRRT 5.mp3"
recognizer.pause_threshold = 0.5

def transcribe_audio(audio_file, recognizer, language="nl-NL"):
    # Provide the path to ffmpeg and ffprobe
    AudioSegment.converter = "/usr/bin/ffmpeg"
    AudioSegment.ffmpeg = "/usr/bin/ffmpeg"
    AudioSegment.ffprobe = "/usr/bin/ffprobe"

    audio = AudioSegment.from_file(audio_file)
    audio.export("temp.wav", format="wav")

    with sr.AudioFile("temp.wav") as source:
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language=language)
          

            # Insert a line break when there's a pause in speech
            pauses = recognizer.pause_threshold
            text_with_line_breaks = ""
            for i, phrase in enumerate(text.split('\n')):
                if i > 0:
                    text_with_line_breaks += '\n'

                text_with_line_breaks += phrase

                # Check if there is a pause between phrases
                if i < len(text.split('\n')) - 1:
                    duration = recognizer.get_duration(audio)
                    if duration > pauses:
                        text_with_line_breaks += '\n'

            return text_with_line_breaks

        except sr.UnknownValueError:
            return "Could not understand audio"

        except sr.RequestError as e:
            return f"Could not request results; {str(e)}"

transcribed_text = transcribe_audio(audio_file, recognizer, language="nl-NL")
print("Transcribed Text: \n" + transcribed_text)
