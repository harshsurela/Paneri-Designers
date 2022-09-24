from scipy.io.wavfile import write
import numpy as np
import fleep
import speech_recognition as sr
from playsound import playsound
playsound("audio.wav")
import numpy as np
import simpleaudio as sa

import pyaudio
import wave

filename = 'audio.wav'

# Set chunk size of 1024 samples per data frame
chunk = 1024  

# Open the sound file 
wf = wave.open(filename, 'rb')

# Create an interface to PortAudio
p = pyaudio.PyAudio()

# Open a .Stream object to write the WAV file to
# 'output = True' indicates that the sound will be played rather than recorded
stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

# Read data in chunks
data = wf.readframes(chunk)

# Play the sound by writing the audio data to the stream
while data != '':
    stream.write(data)
    data = wf.readframes(chunk)

# Close and terminate the stream
stream.close()
p.terminate()


# samplerate = 16000; fs = 100

# t = np.linspace(0., 1., samplerate)

# amplitude = np.iinfo(np.int16).max

# data = amplitude * np.sin(2. * np.pi * fs * t)

# mainfile=write("audio.wav", samplerate, data.astype(np.int16))
# with open("audio.wav", "rb") as file:
#             info = fleep.get(file.read())
#             print(info.type)
#             print(info.extension)
#             print(info.mime)
# r = sr.Recognizer()
# with sr.AudioFile("audio.wav") as source:
#             audio = r.record(source)  
# try:
#     print("The audio file contains: " + str(r.recognize_google(audio, language='en-US', show_all=True)))

# except sr.UnknownValueError:
#     print("Google Speech Recognition could not understand audio")

# except sr.RequestError as e:
#     print("Could not request results from Google Speech Recognition service; {0}".format(e))