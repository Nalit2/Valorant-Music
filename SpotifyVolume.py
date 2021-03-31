import win32gui
from time import sleep
from pycaw.pycaw import AudioUtilities
from threading import Thread

class SpotifyVolume:
    def __init__(self, Resolution):
        self.Resolution = Resolution

        self.White = [(255, 255, 255), (246, 246, 246)]
        self.Tabbed = False
        self.DefaultVolume = self.setDefault()
        self.LowerVolume = 0.3

        self.Volume = self.DefaultVolume

        self.startThreads()

    def startThreads(self):
        Thread(target=self.tabHeld).start()
        Thread(target=self.startScript).start()

    def startScript(self):
        while True:
            result = self.Screenshot()
            if result and self.Volume == self.DefaultVolume:
                self.updateVolume(self.LowerVolume)
            elif not result and self.Volume == self.LowerVolume:
                self.updateVolume(self.DefaultVolume)
            sleep(3)

    def setDefault(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name().lower() == "spotify.exe":
                spotify = session.SimpleAudioVolume
                return spotify.GetMasterVolume()

    def updateVolume(self, volume):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name().lower() == "spotify.exe":
                spotify = session.SimpleAudioVolume
                if self.Volume > volume:
                    for x in range(1, 10):
                        spotify.SetMasterVolume(volume + abs(volume - self.Volume)/x, None)
                        sleep(0.2)
                else:
                    for x in range(1, 10):
                        spotify.SetMasterVolume(
                            volume - abs(volume - self.Volume)/x, None)
                        sleep(0.2)
                self.Volume = volume

    def tabHeld(self):
        from pynput import keyboard

        def keyPress(key):
            if key == keyboard.Key.tab:
                self.Tabbed = True

        def releaseKey(key):
            if key == keyboard.Key.tab:
                self.Tabbed = False

        with keyboard.Listener(
                on_press=keyPress, on_release=releaseKey) as kb:
            kb.join()

    def Screenshot(self):
        from PIL import ImageGrab, Image

        Process = win32gui.GetWindowText(
            win32gui.GetForegroundWindow()).strip(" ")

        if Process != "VALORANT":
            return False

        screenshot = ImageGrab.grab(
            bbox=(int(round(self.Resolution[0] * 0.4192)),
                    int(round(self.Resolution[1] * 0.125)),
                    int(round(self.Resolution[0] * 0.5812)),
                    int(round(self.Resolution[1] * 0.2592))))

        width, height = screenshot.size

        if screenshot.getpixel((0, 0)) == self.White[0] and screenshot.getpixel((0, height-1)) == self.White[1] and screenshot.getpixel((width-1, 0)) == self.White[0] and screenshot.getpixel((width-1, height-1)) == self.White[1]:
            return False
        elif screenshot.getpixel((140, 60)) == self.White[0] and screenshot.getpixel((160, 90)) == self.White[0]:
            return False

        screenshot = ImageGrab.grab(
            bbox=(int(round(self.Resolution[0] * 0.4042)),
                    int(round(self.Resolution[1] * 0.125)),
                    int(round(self.Resolution[0] * 0.5964)),
                    int(round(self.Resolution[1] * 0.26))))

        width, height = screenshot.size

        if screenshot.getpixel((0, 0)) == self.White[0] and screenshot.getpixel((0, height-1)) == self.White[1] and screenshot.getpixel((width-1, 0)) == self.White[0] and screenshot.getpixel((width-1, height-1)) == self.White[1]:
            return False
        else:
            return True
