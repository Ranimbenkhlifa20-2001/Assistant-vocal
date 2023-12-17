import datetime
import sys
import speech_recognition as sr
import pyttsx3 
import wikipediaapi
import wikipedia
from googletrans import Translator
from ecapture import ecapture as ec
import requests
import wolframalpha 
import winshell 
import subprocess 
import ctypes   
import json 
from urllib.request import urlopen 
import pyjokes
import pywhatkit 
import webbrowser
import eel


eel.init('front')

listener= sr.Recognizer()
engine=pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()   


def start():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 6:
        speak("Hey Owl")

    elif hour >= 6 and hour < 12:
        speak("Good Morning")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon")

    else:
        speak("Hello ")

    speak("It's me mark")
    speak("Please tell me how can i help you ?")    


def takeorder():

    listener = sr.Recognizer()
    
    while True:
        with sr.Microphone() as source:
            print("Listening....")
            eel.DisplayMessage('Listening....')
            listener.pause_threshold = 1
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source)

        try:
            print("Recognizing...")
            eel.DisplayMessage('Recognizing....')
            command = listener.recognize_google(audio)
            print(f"You said: {command}")
            eel.DisplayMessage(command)
            return command.lower()

        except sr.UnknownValueError:
            print("Unable to Recognize your voice. Please try again.")
            eel.DisplayMessage("Unable to Recognize your voice. Please try again.")

        except sr.RequestError as e:
            print(f"Error making a request to the speech recognition service: {e}")
            eel.DisplayMessage(f"Error making a request to the speech recognition service: {e}")



def translate_text(text, target_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text



def getnews():

    query_params = {
      "source": "bbc-news",
      "sortBy": "top",
      "apiKey": "your api_key"
    }
    main_url = " https://newsapi.org/v1/articles"
 
    res = requests.get(main_url, params=query_params)
    open_bbc_page = res.json()
 
    article = open_bbc_page["articles"]
 
    results = []
     
    for ar in article [:2]:
        results.append(ar["title"])
         
    for i in range(len(results)):
         
        print(i + 1, results[i])
        eel.DisplayMessage(i + 1, results[i])
        speak(results)    


@eel.expose
def exit():
    speak("I hope that i was useful, thanks for your time, good bye my friend")
    exit()
    


@eel.expose
def allCommands():

    start()
    
    while True :        

        command = takeorder()
        if 'wikipedia' in command:

            speak('Searching Wikipedia...')

            command= command.replace("wikipedia", "")

            results = wikipedia.summary(command, sentences = 2)

            speak("According to Wikipedia")

            print(results)
            eel.DisplayMessage(results)
            speak(results)


        elif 'time' in command:

            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            eel.DisplayMessage(f"the time is {strTime}") 
            speak(f"the time is {strTime}")  
             
 

        elif 'start youtube' in command:
            speak("Here you go my friend")
            webbrowser.open("youtube.com")
 

        elif 'start google' in command:
            speak("Here you go my friend")
            webbrowser.open("google.com")


        elif 'start instagram' in command:
            speak("Here you go my friend")
            webbrowser.open("instagram.com")    


        elif 'joke' in command:
            
            eel.DisplayMessage(pyjokes.get_joke())
            speak(pyjokes.get_joke())  


        elif 'recycle bin' in command:

            winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
            eel.DisplayMessage("Recycle Bin is empty now")
            speak("Recycle Bin is empty now")
    

   
        elif 'how are you' in command:

            speak("I am fine, Thank you, what about you")


        elif 'fine' in  command:

            speak("It's good to know that your fine")        
 

        
        elif 'nice' in command :

            speak("It's good to know that you are satisfied")

          
          
        elif "camera" in command or "take a photo" in command:

            ec.capture(0, "Camera ", "img.jpg")
            eel.DisplayMessage("Done")
            speak("Done")


        elif 'change the background' in command:
            background_path = "C:\\Users\\hp\Desktop\\anime\\img.jpg" 
            ctypes.windll.user32.SystemParametersInfoW(20, 0, background_path, 0)
            eel.DisplayMessage("Background changed successfully")
            speak("Background changed successfully")



        elif "write a note" in command:
            
            eel.DisplayMessage("What should i write")
            speak("What should i write")

            note = takeorder()

            file = open('note.txt', 'w')

            eel.DisplayMessage("Should i include date and time")
            speak("Should i include date and time")

            rep = takeorder()

            if 'yes' in rep :

                strTime = datetime.datetime.now().strftime("%H:%M:%S") 

                file.write(strTime)

                file.write(" :- ")

                file.write(note)

            else:

                file.write(note)

         

        elif 'show me the note' in command:

            eel.DisplayMessage("Showing Notes")
            speak("Showing Notes")

            with open("note.txt", "r") as file:
                note_content = file.read() 

            if note_content:
                eel.DisplayMessage(note_content)
                speak(note_content)
            else:
                eel.DisplayMessage("The note is empty")
                speak("The note is empty.")

        
        elif 'save it ' in command:
            with open("C:\\Users\\hp\\Desktop\\note.txt", "w") as file:
                file.write(note_content)

            eel.DisplayMessage("your note is successfully saved")    
            speak("your note is successfully saved")    


        
        elif "calculate" in command: 

            app_id = "your api_key"

            client = wolframalpha.Client(app_id)

            indx = command.lower().split().index('calculate') 

            query = command.split()[indx + 1:]

            query_str = ' '.join(query)
            res = client.query(query_str)
            try:
              answer = next(res.results).text
              print("The answer is " + answer)
              eel.DisplayMessage("The answer is " + answer)
              speak("The answer is " + answer)

            except StopIteration:
              print("No result found.")
              eel.DisplayMessage("I couldn't find an answer for that")
              speak("I couldn't find an answer for that") 
 
 

        elif "weather" in command:

            api_key = "your api_ki"

            base_url = "https://api.openweathermap.org/data/2.5/weather"

            place = 'tunis'

            complete_url = f"{base_url}?appid={api_key}&q={place}"

            try:
            
               response = requests.get(complete_url)
               response.raise_for_status()  
               data = response.json()  

               temperature = data.get("main", {}).get("temp")
               pressure = data.get("main", {}).get("pressure")
               humidiy = data.get("main", {}).get("humidiy")
    
    
               speak(f"The temperature in {place} is {temperature} Kelvin , the The pressure is {pressure} hPa and  The humidiy  is {humidiy} percent")  

            except requests.exceptions.RequestException as e:
                print(f"Error in request: {e}")
 
      
        elif "what is" in command:

            client = wolframalpha.Client("your api_key")
            res = client.query(command)
             
            try:

               result_text = next(res.results).text
               print(result_text)
               eel.DisplayMessage(result_text)
               speak(result_text)

            except StopIteration:
               print ("i do not know")
               eel.DisplayMessage("i do not know")
               speak("i do not know")   


        elif 'search youtube' in command:
            eel.DisplayMessage("What do you want exactly?")
            speak("What do you want exactly?")
            search = takeorder().lower()
            speak('I found it')
            webbrowser.open('https://www.youtube.com/results?search_query=' + search)


        elif 'search google' in command:
            eel.DisplayMessage('What do you want?')
            speak("What do you want?")
            search = takeorder().lower()
            eel.DisplayMessage('OK here you go')
            speak('OK here you go')
            webbrowser.open('https://www.google.com/search?q=' + search)


        elif ' university website' in command:
            eel.DisplayMessage('OK here you go my friend')
            speak('OK here you go my friend')
            webbrowser.open("http://www.isa2m.rnu.tn/")

        
         
        elif 'translate' in command:
            command = command.replace('translate', '')
            translated_text = translate_text(command)
            eel.DisplayMessage(translated_text)
            speak(translated_text)
            print(translated_text)

        
        elif 'music' in command or 'song' in command or 'play' in command:
            song = command.replace('music', '')
            eel.DisplayMessage("here you go")
            speak('here you go')
            print(song)
            pywhatkit.playonyt(song)


        elif 'news' in command:

            getnews()


        elif 'shut down' in command:

            eel.DisplayMessage("Your system is on its way to shut down")
            speak("Your system is on its way to shut down")
            subprocess.call(["shutdown", "/s"])

     
        
        elif "restart" in command:
            eel.DisplayMessage("Your system is on its way to restart")
            speak("Your system is on its way to restart")
            subprocess.call(["shutdown", "/r"])


        elif 'exit' in command:
            
            eel.DisplayMessage("I hope that i was useful, thanks for your time")
            speak("I hope that i was useful, thanks for your time, good bye my friend")

            exit()   



        eel.sleep(2)
        
    