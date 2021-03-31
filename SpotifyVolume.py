import win32gui
from time import sleep
from pycaw.pycaw import AudioUtilities
from threading import Thread

class SpotifyVolume:
    '''
    Stores all the import variables
    '''
    def __init__(self, Resolution):
        self.Resolution = Resolution

        self.White = [(255, 255, 255), (246, 246, 246)]
        self.Tabbed = False
        self.DefaultVolume = self.setDefault()
        self.LowerVolume = 0.3

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
            elif not result and self.Volume == self.LowerVolume:
                self.updateVolume(self.DefaultVolume)
            sleep(3)

    def setDefault(self):
        '''
        Grabs the current set volume, this is done to make sure the user doesn't get ear damage
        '''
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name().lower() == "spotify.exe":
                spotify = session.SimpleAudioVolume
                return spotify.GetMasterVolume()


    def updateVolume(self, volume):
        '''
        Function to change the volume in a lerp fassion (basiclly smoothly)
        still a bit weird
        '''
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

    def Screenshot(self):
        '''
        Takes the screenshots and determines if the pixels are the color white!
        '''
        from PIL import ImageGrab, Image

        Process = win32gui.GetWindowText(
            win32gui.GetForegroundWindow()).strip(" ")

        if Process != "VALORANT":
            return False

        '''
        The normal buy round image
        '''
        screenshot = ImageGrab.grab(
            bbox=(int(round(self.Resolution[0] * 0.4192)),
                    int(round(self.Resolution[1] * 0.125)),
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
        else:
            return True
