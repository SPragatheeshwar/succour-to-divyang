import os
import speech_recognition as sr
import pyttsx3
from selenium import webdriver
import subprocess
import datetime
import wikipedia
from main import reco

num = 1
def speak(output):
    engine = pyttsx3.init()
    sound = engine.getProperty('voices')
    engine.setProperty('voice', sound[0].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 130)
    engine.say(output)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    audio = ''
    with sr.Microphone() as source:
        print("Speak...")
        audio = r.listen(source, phrase_time_limit=8)
    print("Stop.")

    try:
        said = r.recognize_google(audio, language="en-US")
        print("You:", said)
        return said
    except:
        speak("Sorry, I didn't understand you. Please try again!")
        return 0


def song(input):
    driver = webdriver.Chrome()
    driver.implicitly_wait(1)
    driver.maximize_window()

    if "youtube" in input:
        speak("Opening in youtube")
        indx = input.lower().split().index('youtube')
        query = input.split()[indx + 1:]
        driver.get("http://www.youtube.com/results?search_query =" + '+'.join(query))
        return

    else:
        return


def open_application(input):
    if "chrome" in input:
        speak("Google Chrome")
        os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome')
        return

    elif "firefox" in input or "mozilla" in input:
        speak("Opening Mozilla Firefox")
        os.startfile('C:\Program Files\Mozilla Firefox\firefox.exe')
        return
    else:
        speak("Application not available")
        return


def date():
    date = datetime.datetime.today()
    speak(date)
    return


def weather():
    speak("which city's weather report do you want ?")
    with sr.Microphone() as source:
        r = sr.Recognizer()
        voice = r.listen(source)
        print(voice)
    command = r.recognize_google(voice)
    city = ''
    for i in range(len(command)):
        if i == 0:
            city += command[i].upper()
        else:
            city += command[i]

    driver = webdriver.Chrome(executable_path="D:\chromedriver.exe")
    driver.get("https://www.weather-forecast.com/locations/" + city + "/forecasts/latest")
    a = driver.find_elements_by_class_name("b-forecast__table-description-content")[0].text
    speak(a)
    return


def message(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])
    return



def process_text():
    speak("tell me your command")
    input = get_audio()
    try:

        if 'song' in input or 'play song' in input:
            song(input)
            return
        elif "who are you" in input:
            speak("Hello I am, your personal AI assistant .")
            return

        elif "date" in input or "today's date" in input or "time" in input:
            speak("Here it is.")
            date()
            print("")
            return
        elif "open" in input:
            open_application(input.lower())
            return
        elif "send message" in input:
            speak("what would you like me to note?")
            i = get_audio().lower()
            message(i)
            speak("Done , message sent.")
            return
        elif "wikipedia" in input:
            speak('Searching Wikipedia...')
            input = input.replace("wikipedia", "")
            results = wikipedia.summary(input, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)
            return
        elif "object detection" in input or "image recognition" in input:
            reco()
        elif "weather" in input:
            weather()
            speak("Here it is!")
            print("")
            return

        else:
            speak("I'm sorry , I didn't get you.")

    except:
        speak("Sorry")

while True:
    process_text()

