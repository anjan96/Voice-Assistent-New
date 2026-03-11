# main.py - Full integrated David Assistant with GUI

import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import time
import wikipedia
import pywhatkit
import sys
from requests import get
import yagmail
from tkinter import *
from PIL import ImageTk, Image
import threading

# ---------------- TTS ----------------
def speak(text):
    """Speak text using pyttsx3 safely on Windows"""
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)  # pause to prevent mic picking up own voice

# ---------------- Greet User ----------------
def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        greet = "Good Morning"
    elif hour < 18:
        greet = "Good Afternoon"
    else:
        greet = "Good Evening"
    speak(f"{greet} sir, I am your assistant David. How can I help you?")

# ---------------- Listen ----------------
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
        except sr.WaitTimeoutError:
            return ""
    try:
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Sorry, I cannot connect to Google. Check your internet.")
        return ""

# ---------------- Email Functionality ----------------
# Replace 'your-app-password' with your 16-character Gmail App Password
yag = yagmail.SMTP('anjan.private01@gmail.com', 'gflp drnv itue nnzj')

def send_email(to, content, recipient_name):
    if content:
        try:
            yag.send(to, f"Email from David Assistant", content)
            speak(f"Email has been sent to {recipient_name}")
        except Exception as e:
            print(e)
            speak(f"Sorry sir, I am unable to send email to {recipient_name}")
    else:
        speak("No content received. Email not sent.")

def emailToAnjan():
    speak("What should I say in the email to Anjan?")
    content = listen_command()
    send_email("anjan.nwu@gmail.com", content, "Anjan")

def emailToRashmi():
    speak("What should I say in the email to Rashmi?")
    content = listen_command()
    send_email("rasmyakter227@gmail.com", content, "Rashmi")

def emailToNadeem():
    speak("What should I say in the email to Nadeem?")
    content = listen_command()
    send_email("nadimsamratbd@gmail.com", content, "Nadeem")

# ---------------- Process Queries ----------------
def process_query(query):
    if 'time' in query:
        speak(f"The time is {datetime.datetime.now().strftime('%I:%M %p')}")
    elif 'date' in query:
        speak(f"Today is {datetime.datetime.now().strftime('%Y-%m-%d')}")
    elif 'your name' in query or 'introduce yourself' in query or 'hey david' in query:
        speak("I am David, your personal assistant. I can help you open apps, send emails, search online, and play music.")
    elif 'wikipedia' in query:
        speak("What should I search on Wikipedia?")
        search_query = listen_command()
        if search_query:
            speak(f"Searching Wikipedia for {search_query}")
            try:
                results = wikipedia.summary(search_query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except Exception:
                speak("Sorry sir, I could not find any information.")
        else:
            speak("No query received for Wikipedia search.")

    elif 'search' in query:
        query_text = query.replace("search", "").strip()
        speak(f"Searching {query_text}")
        pywhatkit.search(query_text)
    elif 'open google' in query:
        speak("Sir, what should I search for?")
        search = listen_command()
        webbrowser.open(f"https://www.google.com/search?q={search}")
        speak(f"Opening Google search for {search}")
    elif 'open youtube' in query:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif 'open facebook' in query:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif 'open instagram' in query:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
    elif 'open stack overflow' in query:
        speak("Opening Stack Overflow")
        webbrowser.open("https://www.stackoverflow.com")
    elif 'open github' in query:
        speak("Opening GitHub")
        webbrowser.open("https://www.github.com")
    elif 'play music' in query:
        music_directory = 'E:\\music'  # update path as needed
        try:
            songs = os.listdir(music_directory)
            if songs:
                speak("Playing music")
                os.startfile(os.path.join(music_directory, songs[0]))
            else:
                speak("No music found in directory")
        except Exception:
            speak("Unable to play music")
    elif "open notepad" in query:
        speak("Opening Notepad")
        os.startfile("C:\\windows\\system32\\notepad.exe")
    elif "open chrome" in query:
        speak("Opening Chrome")
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    elif "open code block" in query:
        speak("Opening CodeBlocks")
        os.startfile("C:\\Program Files (x86)\\CodeBlocks\\codeblocks.exe")
    elif "open powerpoint" in query:
        speak("Opening PowerPoint")
        os.startfile("C:\\Program Files (x86)\\Microsoft Office\\Office15\\POWERPNT.EXE")
    elif "open ms word" in query:
        speak("Opening Word")
        os.startfile("C:\\Program Files (x86)\\Microsoft Office\\Office15\\WINWORD.EXE")
    elif "open excel" in query:
        speak("Opening Excel")
        os.startfile("C:\\Program Files (x86)\\Microsoft Office\\Office15\\EXCEL.EXE")
    elif "open zoom" in query:
        speak("Opening Zoom")
        os.startfile("C:\\Users\\Anjan\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe")
    elif "open command prompt" in query:
        speak("Opening Command Prompt")
        os.system("start cmd")
    elif "email to anjan" in query:
        emailToAnjan()
    elif "email to nadeem" in query:
        emailToNadeem()
    elif "email to rashmi" in query:
        emailToRashmi()
    elif "ip address" in query:
        try:
            ip = get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")
        except Exception:
            speak("Unable to fetch IP address")
    elif "stop" in query or "exit" in query:
        speak("Thanks for using me sir, have a good day.")
        return False
    else:
        speak("Sorry sir, I cannot perform this command yet.")
    return True

# ---------------- Main Loop ----------------
def main():
    greet_user()
    running = True
    while running:
        query = listen_command()
        if not query:
            continue
        # Only respond if user says 'david'
        if "david" in query:
            query = query.replace("david", "").strip()
            running = process_query(query)
        time.sleep(0.3)  # pause before next listen

# ---------------- GUI Setup ----------------
def main_thread():
    threading.Thread(target=main).start()

def setup_gui():
    window = Tk()
    window.title("Voice Assistant")
    window.geometry("500x470")
    window.config(background="#5cfcff")

    label1 = Label(window, text="Voice Assistant", font="Arial 20 bold", fg='#00ff00', bg='black', justify="center")
    label1.pack()

    try:
        image = ImageTk.PhotoImage(file='pic.jpg')  # Make sure pic.jpg is in same folder
        label2 = Label(window, image=image)
        label2.image = image  # Keep reference
        label2.place(x=0, y=141)
    except Exception as e:
        print("Error loading image:", e)

    Button(window, text="Start Listening", font="Arial 12 bold", fg="white", bg="green",
           command=main_thread).pack(pady=10)

    window.mainloop()

# ---------------- Entry Point ----------------
if __name__ == "__main__":
    setup_gui()
