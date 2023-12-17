import os
import eel
from engine.sound import *
from engine.commandes import *
import threading


def start_eel_app():
    eel.init('front')
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host='localhost', block=True)


if __name__ == '__main__':
    playAssistantSound()
    eel_thread = threading.Thread(target=start_eel_app)
    eel_thread.start()

    allCommands()

