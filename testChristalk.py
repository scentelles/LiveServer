from SmoothDefines import *
import time
from pythonosc import udp_client

#sendosc 10.3.141.1 5005 /step_next i 255

#OSC connection to QLC+
clientQLC = udp_client.SimpleUDPClient("10.3.141.1", 8000)

#First set a progam change corresponding to Smooth range
#clientQLC.send_message("/midi/voicelive", [MIDI_PROGRAM_CHANGE, SMOOTH_PRESET_ANOTHER_TOWN, 0])
#
#time.sleep(2)

clientQLC.send_message("/midi/voicelive", [MIDI_CONTROL_CHANGE, MIDI_CONTROL_CHANGE_FROM_CHRIS, MIDI_CC_CHRIS_TALK])


