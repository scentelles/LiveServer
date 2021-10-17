import socket
import sys  
sys.path.append("..")  

from SmoothDefines import *
import time
from pythonosc import udp_client

#OSC connection to Video manager
#LOCALHOST_IP   = "192.168.1.51"
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(local_ip)

LOCALHOST_IP   =    local_ip
LOCALHOST_PORT = 5007

clientVideoPC = udp_client.SimpleUDPClient(LOCALHOST_IP, LOCALHOST_PORT)

DELAY = 1



	
def testSlideSelection(song_id):
    print ("\n\nTEST : Slide selection of song " + str(song_id) + "(" + SName[song_id]  + ")" + " \n")  
    clientVideoPC.send_message("/video/song", song_id)


for song_id in SName.keys():
    testSlideSelection(song_id)
    time.sleep(1)
    clientVideoPC.send_message("/video/slideshow", SLIDESHOW_COMMAND_NEXT_SLIDE)
    time.sleep(0.5)
    clientVideoPC.send_message("/video/slideshow", SLIDESHOW_COMMAND_NEXT_SLIDE)
    time.sleep(2)    