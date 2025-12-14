# -*- coding: utf-8 -*-
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import webbrowser
import time

# Initialize the recognizer
listener = sr.Recognizer()

def talk(text):
    """Speak the given text aloud."""
    print(f"Assistant: {text}")
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def take_command():
    """Listen to user's voice and return the command as text."""
    try:
        with sr.Microphone() as source:
            print("\nListening... please speak now.")
            listener.adjust_for_ambient_noise(source, duration=1)
            audio = listener.listen(source, timeout=5, phrase_time_limit=7)
            print("✅ Voice captured, recognizing...")
            command = listener.recognize_google(audio)
            command = command.lower()
            if 'assistant' in command:
                command = command.replace('assistant', '').strip()
            return command
    except sr.UnknownValueError:
        talk("Sorry, I could not understand that.")
        return ""
    except sr.RequestError:
        talk("Sorry, my speech service is unavailable right now.")
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

def greet_user():
    """Dynamic greeting based on the time of day."""
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        greet = "Good morning!"
    elif 12 <= hour < 18:
        greet = "Good afternoon!"
    elif 18 <= hour < 22:
        greet = "Good evening!"
    else:
        greet = "Hello!"
    talk(f"{greet} I am your voice assistant. How can I help you today?")

def run_assistant():
    """Main function to process user commands."""
    command = take_command()
    if not command:
        return
    print(f"You said: {command}")

    # ---- Command Handling ----
    if 'play' in command:
        song = command.replace('play', '').strip()
        if song:
            talk(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)
        else:
            talk("Please say the song name after 'play'.")

    elif 'time' in command:
        time_now = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The current time is {time_now}")

    elif 'open youtube' in command:
        talk("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif 'open google' in command:
        talk("Opening Google")
        webbrowser.open("https://www.google.com")

    elif 'open github' in command:
        talk("Opening GitHub")
        webbrowser.open("https://www.github.com")

    elif 'hello' in command or 'hi' in command:
        talk("Hello there! How can I assist you today?")

    elif 'stop' in command or 'exit' in command or 'bye' in command:
        talk("Goodbye! Have a great day!")
        exit()

    else:
        talk("Sorry, I didn't catch that. Please say it again.")

    # Short pause before next listening cycle
    time.sleep(1)

# ------------------ MAIN PROGRAM ------------------
if __name__ == "__main__":
    greet_user()
    while True:
        run_assistant()
