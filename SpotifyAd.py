import win32gui
from time import sleep
from ctypes import windll
from pycaw.pycaw import AudioUtilities
from threading import Thread
from psutil import process_iter, NoSuchProcess, AccessDenied, ZombieProcess

class SpotifyAd:
    def __init__(self):
        self.Title = ""
        self.muted = False

        Thread(target=self.muteAd()).start()

    def isAlive(self, processName):
        for proc in process_iter():
            try:
                if processName.lower() in proc.name().lower():
                    return True
            except (NoSuchProcess, AccessDenied, ZombieProcess):
                pass
        return False

    def setTitle(self):
        Title = []

        def enumWindowsProc(hwnd, lParam):
            if win32gui.GetWindowText(hwnd) != "":
                if windll.user32IsWindowVisible(hwnd):
                    Title.append(win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(enumWindowsProc, 0)
        return Title

    def muteAd(self):
        while True:
            if self.isAlive("spotify"):
                sleep(1)
                if "Advertisement" in self.setTitle() and not self.muted:
                    self.muted = True
                    sessions = AudioUtilities.GetAllSessions()
                    for session in sessions:
                        if session.Process and session.Process.name().lower() == "spotify.exe":
                            spotify = session.SimpleAudioVolume
                            spotify.SetMute(1, None)
                elif "Advertisement" not in self.setTitle() and self.muted:
                    self.muted = False
                    sessions = AudioUtilities.GetAllSessions()
                    for session in sessions:
                        if session.Process and session.Process.name().lower() == "spotify.exe":
                            spotify = session.SimpleAudioVolume
                            spotify.SetMute(0, None)
