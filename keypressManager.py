from pynput.keyboard import Key, Listener
import socket 
from pythonosc import udp_client

from SmoothDefines import *


hostname = socket.gethostname()
videoPC_ip = socket.gethostbyname(hostname)
clientVideoPC = udp_client.SimpleUDPClient(videoPC_ip, 5007)


def on_release(key):
    print('{0} release'.format(key))
    if key == Key.esc:
        return False
    if (key == Key.up):
        print("Next slide")
        clientVideoPC.send_message("/video/slideshow", SLIDESHOW_COMMAND_NEXT_SLIDE)
    if (key == Key.down):
        print("Previous slide")
        clientVideoPC.send_message("/video/slideshow", SLIDESHOW_COMMAND_PREVIOUS_SLIDE)    
        
with Listener(on_release=on_release) as listener:
    listener.join()