from SmoothDefines import *
import time
from pythonosc import udp_client

#sendosc 10.3.141.1 5005 /step_next i 255

#OSC connection to QLC+
clientQLC = udp_client.SimpleUDPClient("10.3.141.1", 8000)

clientQLC.send_message("/midi/voicelive", [0xb0, 0x20, 1])


