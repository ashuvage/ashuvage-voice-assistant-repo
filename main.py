import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import openai 
import os
from gtts import gTTS
import pygame
import time


recognizer = sr.Recognizer()
engine = pyttsx3.init()

#Setup the API keys

newsApi = ("3bef8cab51154f7baa410f2064998c64")
client = openai.OpenAI(api_key="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")
def speak_tts(text):
    engine.say(text)
    engine.runAndWait()

def speak_gtts(text):
    try:
        tts = gTTS(text=text, lang='en')
        temp_path = "temp_audio.mp3"
        tts.save(temp_path)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        pygame.mixer.quit()

        os.remove(temp_path)
    except Exception as e:
        print(f"gTTS error: {e}") 

USE_GTTS = True # or false to use pyttsx3

def speak(text):
    if USE_GTTS:
        speak_gtts(text)
    else:
        speak_tts(text)



def aiprocess(command):
    
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "you are a virtual assistant named jarvis skilled in general tasks like alexa and google cloud"},
            {"role": "user", "content": command}
        ]
    )    
    return response.choices[0].message.content


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")

    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        if link:
            webbrowser.open(link)
        else:
            speak("sorry, i couldn't find the song ")    

    elif "news" in c:        
        # Send a GET request to the news API
        api_url = ("https://newsapi.org/v2/top-headlines?country=in&apiKey=3bef8cab51154f7baa410f2064998c64")
        r = requests.get(api_url)
        if r.status_code == 200:
            data = r.json()
           

        # Get the list of articles
            articles = data.get("articles", [])

        # Print each headline
            if articles:

                for article in articles[:5]:
                    if article.get("title"):
                        speak(article["title"])

            else:
                speak("sorry, I couldn't fetch the news right now")  

        else:
            speak("no articles found")        

    
    
    else:
        output = aiprocess(c)
        speak(output)


      

if __name__ == "__main__":
    speak("initializing jarvis.............")
    while True:
      
    
        try:
            with sr.Microphone() as source:
                
                print("listening......")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)

                print("Recognizing......")
            
                word = recognizer.recognize_google(audio)
            if word.lower()=="jarvis":
                speak("ohh yeah!")
                #Listen for the command
                with sr.Microphone() as source:
                    print(" jarvis Active.... ")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)

                    processCommand(command)
      

            

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        
       
        except sr.WaitTimeoutError:
            print(" Listening timed out while waitng for phrase to start")  
