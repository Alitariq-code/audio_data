import os
import speech_recognition as sr
from pydub import AudioSegment  # Add this import statement

# Initialize the recognizer
recognizer = sr.Recognizer()

# List of audio files
audio_files = [
    "/home/alicode/Desktop/audio data/AVI 5.wav",
    "/home/alicode/Desktop/audio data/AVI 3.wav"
]

# Output file for saving results
output_file = "/home/alicode/Desktop/audio data/results.txt"

with open(output_file, 'w') as output:
    for audio_file in audio_files:
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
                text = recognizer.recognize_google(audio, language="nl-NL")

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

                # Write the results to the output file
                output.write(f"Transcription for {audio_file}:\n{text_with_line_breaks}\n\n")

            except sr.UnknownValueError:
                output.write(f"Could not understand audio for {audio_file}\n\n")

            except sr.RequestError as e:
                output.write(f"Could not request results for {audio_file}; {str(e)}\n\n")

# Print a message indicating the transcription is complete
print(f"Transcription complete. Results saved in {output_file}")
