import speech_recognition as sr
from pydub import AudioSegment
recognizer = sr.Recognizer()
audio_file = "/home/alicode/Desktop/audio data/WRRT 5.mp3"
audio = AudioSegment.from_file(audio_file)
audio.export("temp.wav", format="wav")
with sr.AudioFile("temp.wav") as source:
    recognizer.adjust_for_ambient_noise(source)
    try:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language="nl-NL")
        pauses = recognizer.pause_threshold
        text_with_line_breaks = ""
        for i, phrase in enumerate(text.split('\n')):
            if i > 0:
                text_with_line_breaks += '\n'
            text_with_line_breaks += phrase
            if i < len(text.split('\n')) - 1:
                duration = recognizer.get_duration(audio)
                if duration > pauses:
                    text_with_line_breaks += '\n'
        print("Transcribed Text:\n" + text_with_line_breaks)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results; {str(e)}")