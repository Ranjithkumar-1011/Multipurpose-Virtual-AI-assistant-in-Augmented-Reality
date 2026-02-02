import socket
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import time
import os
from github import Github

# ----------------------------------
# GITHUB SETUP
# ----------------------------------

github_token = os.getenv('GITHUB_TOKEN')
if github_token:
    g = Github(github_token)
else:
    g = None

# ----------------------------------
# UNITY SOCKET CONNECTION
# ----------------------------------

server = socket.socket()
server.bind(("localhost", 9999))
server.listen(1)

print("Waiting for Unity...")
conn, addr = server.accept()
print("Unity connected ✅")

def send_to_unity(msg):
    try:
        conn.send((msg + "\n").encode())
        time.sleep(0.05)   # VERY IMPORTANT
    except:
        pass


# ----------------------------------
# VOICE SETUP
# ----------------------------------

listener = sr.Recognizer()

def create_engine():
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)
    return engine

machine = create_engine()


# ----------------------------------
# LISTEN FUNCTION
# ----------------------------------

def listen(seconds=5):
    fs = 16000

    recording = sd.rec(
        int(seconds * fs),
        samplerate=fs,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    audio = sr.AudioData(
        recording.tobytes(),
        fs,
        2
    )

    try:
        text = listener.recognize_google(audio)
        print("You:", text)
        return text.lower()
    except:
        return ""


# ----------------------------------
# SPEAK FUNCTION (FIXED)
# ----------------------------------

def talk(text):
    print("Jarvis:", text)

    send_to_unity("TALK")

    machine.say(text)
    machine.runAndWait()

    time.sleep(0.3)
    #allow animation to play
    send_to_unity("IDLE")


# ----------------------------------
# INPUT FUNCTION
# ----------------------------------

def input_instruction():
    send_to_unity("LISTEN")
    command = listen(5)
    send_to_unity("IDLE")

    if "jarvis" in command:
        command = command.replace("jarvis", "")

    return command.strip()


# ----------------------------------
# MAIN LOGIC
# ----------------------------------

def play_jarvis():

    instruction = input_instruction()

    if instruction == "":
        return

    if "play" in instruction:
        song = instruction.replace("play", "")
        talk("Playing " + song)
        pywhatkit.playonyt(song)

    elif "time" in instruction:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        talk("Current time " + time_now)

    elif "date" in instruction:
        date_now = datetime.datetime.now().strftime("%d %B %Y")
        talk("Today's date is " + date_now)

    elif "how are you" in instruction:
        talk("I am fine. How about you")

    elif "what is your name" in instruction:
        talk("I am Jarvis. Your virtual assistant")

    elif "who is" in instruction:
        human = instruction.replace("who is", "")
        try:
            info = wikipedia.summary(human, 1)
            talk(info)
        except:
            talk("Sorry. I couldn't find information")

    elif "check github" in instruction or "github status" in instruction:
        if g:
            user = g.get_user()
            talk(f"Connected to GitHub as {user.login}")
        else:
            talk("GitHub not connected. Please set GITHUB_TOKEN environment variable")

    elif "list repos" in instruction or "my repos" in instruction:
        if g:
            user = g.get_user()
            repos = user.get_repos()
            repo_names = [repo.name for repo in repos[:5]]  # Limit to 5
            talk(f"Your top repositories: {', '.join(repo_names)}")
        else:
            talk("GitHub not connected")

    elif "stop" in instruction or "exit" in instruction:
        talk("Shutting down. Goodbye")
        exit()

    else:
        talk("Please repeat")


# ----------------------------------
# RUN
# ----------------------------------

while True:
    play_jarvis()
