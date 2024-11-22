

import speech_recognition as sr
import webbrowser
import pyttsx3
import music_lib
from openai import OpenAI  # Ensure the OpenAI library is installed (pip install openai)

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# OpenAI API Key (replace <Your Key Here> with your actual API key)
API_KEY = "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"

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to process AI requests using OpenAI
def aiProcess(command):
    client = OpenAI(api_key=API_KEY)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named D skilled in general tasks like Alexa and Google Cloud. Give short responses, please."},
            {"role": "user", "content": command},
        ],
    )
    return completion.choices[0].message.content

# Function to listen for wake word "Doodle"
def listen_for_wakeup():
    print("Listening for wake word...")
    speak("Listening for the wake word.")
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            print("Waiting for 'Doodle'...")
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio).lower()
                print(f"Heard: {command}")
                if "Doodle" in command:
                    speak("Doodle activated!")
                    start_listening_for_commands()
                    break
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

# Function to listen for and process commands
def start_listening_for_commands():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            print("Listening for your command...")
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                
                if "open google" in command:
                    speak("Opening Google")
                    webbrowser.open("https://www.google.com")
                elif command.startswith("play"):
                    song = command.split(" ", 1)[1]
                    if song in music_lib.music:
                        speak(f"Playing {song}")
                        webbrowser.open(music_lib.music[song])
                    else:
                        speak(f"Sorry, I couldn't find {song} in your music library.")
                elif "open facebook" in command:
                    speak("Opening Facebook")
                    webbrowser.open("https://www.facebook.com")
                elif "exit" in command:
                    speak("Goodbye!")
                    exit()
                else:
                    # Let OpenAI handle the request
                    output = aiProcess(command)
                    speak(output)
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

# Start the wake-up listening process
listen_for_wakeup()






