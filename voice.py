import pyttsx3
import sounddevice as sd
import numpy as np
import speech_recognition as sr

# ---------- SPEECH RECOGNITION ----------

recognizer = sr.Recognizer()

def listen():
    duration = 5
    samplerate = 16000

    print("Listening...")

    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="int16"
    )
    sd.wait()

    audio_bytes = audio.tobytes()

    audio_data = sr.AudioData(audio_bytes, samplerate, 2)

    try:
        text = recognizer.recognize_google(audio_data)
        print("You:", text)
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

# ---------- TEXT TO SPEECH ----------

def speak(text):
    print("Jarvis:", text)

    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)

    engine.say(text)
    engine.runAndWait()

    engine.stop()
