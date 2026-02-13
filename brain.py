import datetime
import wikipedia
import pywhatkit
from voice import speak,listen
from socket_server import SocketServer
import time



def process(command):
    if "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)

    elif "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time}")

    elif "date" in command:
        date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {date}")

    elif "who is" in command:
        person = command.replace("who is", "").strip()
        try:
            info = wikipedia.summary(person, sentences=2)
            speak(info)
        except wikipedia.exceptions.DisambiguationError:
            speak(f"There are multiple results for {person}. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak(f"I could not find information about {person}.")


    elif "exit" in command or "stop" in command:
        speak("Shutting down. Goodbye.")
        return False

    else:
        speak("I did not understand that.")

    return True

def main():
    socket_server = SocketServer()

    speak("Jarvis activated")
    socket_server.send("IDLE")

    running = True

    while running:
        socket_server.send("LISTEN")
        command = listen()

        if command:
            socket_server.send("TALK")
            running = process(command)
            time.sleep(1.2)
            socket_server.send("IDLE")

if __name__ == "__main__":
    main()
