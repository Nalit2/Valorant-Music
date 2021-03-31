import win32gui, time, ctypes
from pycaw.pycaw import AudioUtilities
import multiprocessing, threading
import psutil

Resolution = input("Example (1920x1080)\nResolution: ").split("x")
Resolution = [int(Resolution[0]), int(Resolution[1])]

class ValorantSpotify:
    class SpotifyAd:
        def __init__(self):
            self.Title = ""
            self.SpotifyPointer = "GDI+ Window (Spotify.exe)"
            self.muted = False

            multiprocessing.Process(target=self.muteAd).start()

        def isAlive(self, processName):
            for proc in psutil.process_iter():
                try:
                    if processName.lower() in proc.name().lower():
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            return False
        def setTitle(self):
            Title = []

            def enumWindowsProc(hwnd, lParam):
                if win32gui.GetWindowText(hwnd) != "":
                    if ctypes.windll.user32.IsWindowVisible(hwnd):
                        Title.append(win32gui.GetWindowText(hwnd))
            win32gui.EnumWindows(enumWindowsProc, 0)
            return Title
                
        def muteAd(self):
            while True:
                if self.isAlive("spotify"):
                    time.sleep(1)
                    if "Advertisement" in self.setTitle() and not self.muted:
                        sessions = AudioUtilities.GetAllSessions()
                        for session in sessions:
                            if session.Process and session.Process.name().lower() == "spotify.exe":
                                spotify = session.SimpleAudioVolume
                                spotify.SetMute(1, None)
                    elif "Advertisement" not in self.setTitle() and self.muted:
                        sessions = AudioUtilities.GetAllSessions()
                        for session in sessions:
                            if session.Process and session.Process.name().lower() == "spotify.exe":
                                spotify = session.SimpleAudioVolume
                                spotify.SetMute(0, None)

    class SpotifyVolume:
        def __init__(self):
            self.White = [(255, 255, 255), (246, 246, 246)]
            self.Tabbed = False
            self.DefaultVolume = self.setDefault()
            self.LowerVolume = 0.3

            self.Volume = self.DefaultVolume

            self.startThreads()

        def startThreads(self):
            threading.Thread(target=self.tabHeld).start()
            threading.Thread(target=self.startScript).start()

        def startScript(self):
            while True:
                result = self.Screenshot()
                if result and self.Volume == self.DefaultVolume:
                    self.updateVolume(self.LowerVolume)
                elif not result and self.Volume == self.LowerVolume:
                    self.updateVolume(self.DefaultVolume)
                time.sleep(3)

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
                            time.sleep(0.2)
                    else:
                        for x in range(1, 10):
                            spotify.SetMasterVolume(
                                volume - abs(volume - self.Volume)/x, None)
                            time.sleep(0.2)
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
                bbox=(int(round(Resolution[0] * 0.4192)),
                      int(round(Resolution[1] * 0.125)),
                      int(round(Resolution[0] * 0.5812)),
                      int(round(Resolution[1] * 0.2592))))

            width, height = screenshot.size
            
            if screenshot.getpixel((0, 0)) == self.White[0] and screenshot.getpixel((0, height-1)) == self.White[1] and screenshot.getpixel((width-1, 0)) == self.White[0] and screenshot.getpixel((width-1, height-1)) == self.White[1]:
                return False
            elif screenshot.getpixel((140, 60)) == self.White[0] and screenshot.getpixel((160, 90)) == self.White[0]:
                return False

            screenshot = ImageGrab.grab(
                bbox=(int(round(Resolution[0] * 0.4042)), 
                      int(round(Resolution[1] * 0.125)), 
                      int(round(Resolution[0] * 0.5964)), 
                      int(round(Resolution[1] * 0.26))))
            
            width, height = screenshot.size

            if screenshot.getpixel((0, 0)) == self.White[0] and screenshot.getpixel((0, height-1)) == self.White[1] and screenshot.getpixel((width-1, 0)) == self.White[0] and screenshot.getpixel((width-1, height-1)) == self.White[1]:
                return False
            else:
                return True


def StartAdblocker():
    ValorantSpotify().SpotifyAd()

if __name__=='__main__':
    multiprocessing.Process(target=StartAdblocker).start()
    ValorantSpotify().SpotifyVolume()
