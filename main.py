from multiprocessing import Process

Resolution = input("Example (1920x1080)\nResolution: ").split("x")
Resolution = [int(Resolution[0]), int(Resolution[1])]

def StartAdblocker():
    from SpotifyAd import SpotifyAd
    SpotifyAd()
    
if __name__=='__main__':
    Process(target=StartAdblocker).start()
    
    from SpotifyVolume import SpotifyVolume
    SpotifyVolume(Resolution)
