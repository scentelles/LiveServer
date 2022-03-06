import sys  
sys.path.append("..")  

from SmoothDefines import *
import time
from pythonosc import udp_client

LOCALHOST_IP   = "127.0.0.1"
LOCALHOST_PORT = 7700

clientProjectM = udp_client.SimpleUDPClient(LOCALHOST_IP, LOCALHOST_PORT)

DELAY = 1

clientProjectM.send_message("/projectm/preset", 2)
