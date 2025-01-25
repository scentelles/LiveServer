#!/usr/bin/python3
import sys

LHPreset = sys.argv[1]
print (LHPreset)

from pythonosc import udp_client
clientLH = udp_client.SimpleUDPClient("10.3.141.90", 8001)
clientLH.send_message("/laserharp/startLH", int(LHPreset))
