from threading import Thread
import os, time

while True:
    Resolution = input("Example (1920x1080)\nResolution: ")

    if "x" not in Resolution:
        print("Please input a resolution")
        time.sleep(1)
        os.system("CLS")
    else:     
        Resolution = Resolution.split("x")
        Resolution = [int(Resolution[0]), int(Resolution[1])]
        break

while True:
    '''
    Ugly I know, not sure how to do it without going overkill
    '''
    Type = input("Spotify or Youtube: ")
    if "yt" not in Type.lower() and "youtube" not in Type.lower() and "sp" not in Type.lower() and "spotify" not in Type.lower():
        print("Please input Youtube | yt or Spotify | sp")
        time.sleep(1)
        os.system("CLS")
    else:
        break

os.system("CLS")
print("Started application")
        
if __name__ == '__main__':
    if Type.lower() != "yt" and Type.lower() != "youtube":
        from SpotifyAd import SpotifyAd
        Thread(target=SpotifyAd).start()
    
    from SpotifyVolume import SpotifyVolume
    SpotifyVolume(Resolution, Type.lower())
