import win32gui
from time import sleep
from pycaw.pycaw import AudioUtilities
from threading import Thread
from PIL import ImageGrab, Image
import sys

class SpotifyVolume:
    '''
    Stores all the import variables
    '''
    def __init__(self, Resolution, Type):
        self.Resolution = Resolution
        '''
        Check if its youtube or spotify
        ''' 
        self.applications = ["opera.exe", "chrome.exe", "brave.exe", "firefox.exe",
                             "msedge.exe" if Type == "yt" or Type == "youtube" else "spotify.exe"]
        
        self.White = [(255, 255, 255), (246, 246, 246)]
        self.Tabbed = False
        self.DefaultVolume = self.setDefault()
        self.LowerVolume = 0.1

        self.Volume = self.DefaultVolume

        self.startThreads()

    def startThreads(self):
        '''
        starts all the required threads
        this is needed because of sleep functions can overlap each other
        '''
        Thread(target=self.tabHeld).start()
        Thread(target=self.startScript).start()

    def startScript(self):
        '''
        The loop that keeps checking to see if you are in the middle of a round
        or in the buy phase
        '''
        while True:
            result = self.Screenshot()
            if result and self.Volume == self.DefaultVolume:
                self.updateVolume(self.LowerVolume)
                print("Lowering volume")
            elif not result and self.Volume == self.LowerVolume:
                self.updateVolume(self.DefaultVolume)
                print("Rasing volume")
            sleep(3)

    def setDefault(self):
        '''
        Grabs the current set volume, this is done to make sure the user doesn't get ear damage
        '''
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name().lower() in self.applications:
                spotify = session.SimpleAudioVolume
                return spotify.GetMasterVolume()


    def updateVolume(self, volume):
        '''
        Function to change the volume in a lerp fassion (basiclly smoothly)
        still a bit weird
        '''
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            '''
            One issue that can occur is having multiple browsers open, the app will pick the first
            browser that windows media player returns
            '''
            if session.Process and session.Process.name().lower() in self.applications:
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
        '''
        When tab is held, the music will be pushed back up to loud volume
        this happens because the reference point is removed when tab is held
        in-game.
        
        '''
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
    
    def inMatch(self) -> bool:
        screenshot = ImageGrab.grab(
            bbox=(int(round(self.Resolution[0] * 0.4947)),
                  int(round(self.Resolution[1] * 0.0398)),
                  int(round(self.Resolution[0] * 0.4963)),
                  int(round(self.Resolution[1] * 0.0555))))
        
        width, height = screenshot.size

        return True if screenshot.getpixel((1, 1)) == self.White[0] and screenshot.getpixel((width-1, height-1)) == self.White[0] else False

    def isDead(self) -> bool:
        screenshot = ImageGrab.grab(
            bbox=(int(round(self.Resolution[0] * 0.8385)),
                  int(round(self.Resolution[1] * 0.3703)),
                  int(round(self.Resolution[0] * 0.8593)),
                  int(round(self.Resolution[1] * 0.3713))))

        width, height = screenshot.size

        if screenshot.getpixel((0, 0)) == self.White[0] and screenshot.getpixel((width-1, height-1)) == self.White[0]:
            return True  
        else:
            return False

    def Screenshot(self):
        '''
        Takes the screenshots and determines if the pixels are the color white!
        '''
        if not self.inMatch():
            return False

        Process = win32gui.GetWindowText(
            win32gui.GetForegroundWindow()).strip(" ")

        if Process != "VALORANT":
            return False

        '''
        The normal buy round image
        '''
        screenshot = ImageGrab.grab(
            bbox=(int(round(self.Resolution[0] * 0.4192)),
                  int(round(self.Resolution[1] * 0.1250)),
                  int(round(self.Resolution[0] * 0.5812)),
                  int(round(self.Resolution[1] * 0.2592))))

        width, height = screenshot.size

        if screenshot.getpixel((0, 0)) == self.White[0] and screenshot.getpixel((0, height-1)) == self.White[1] and screenshot.getpixel((width-1, 0)) == self.White[0] and screenshot.getpixel((width-1, height-1)) == self.White[1]:
            return False
        elif screenshot.getpixel((140, 60)) == self.White[0] and screenshot.getpixel((160, 90)) == self.White[0]:
            '''
            This one sees if you picked up the spike, because picking up the spike
            also removes the reference point
            '''
            return False

        '''
        Match point Image
        '''
    
        screenshot = ImageGrab.grab(
            bbox=(int(round(self.Resolution[0] * 0.4042)),
                  int(round(self.Resolution[1] * 0.125)),
                  int(round(self.Resolution[0] * 0.5964)),
                  int(round(self.Resolution[1] * 0.26))))

        width, height = screenshot.size

        if screenshot.getpixel((0, 0)) == self.White[0] and screenshot.getpixel((0, height-1)) == self.White[1] and screenshot.getpixel((width-1, 0)) == self.White[0] and screenshot.getpixel((width-1, height-1)) == self.White[1]:
            return False
        elif self.isDead():
            return False
        else:
            return True
