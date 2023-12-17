from playsound import playsound
import eel

# Playing assiatnt sound function

@eel.expose
def playAssistantSound():
    music_dir = "front\\assets\\sound\\start_sound.mp3"
    playsound(music_dir)
