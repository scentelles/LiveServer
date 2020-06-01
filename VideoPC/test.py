import sys  
sys.path.append("..")  

from SmoothDefines import *
import time
from pythonosc import udp_client

#OSC connection to Video manager
LOCALHOST_IP   = "192.168.1.51"
LOCALHOST_PORT = 5007
clientVideoPC = udp_client.SimpleUDPClient(LOCALHOST_IP, LOCALHOST_PORT)

DELAY = 1

MIDI_CONTROL_CHANGE = 0xb0
MIDI_PROGRAM_CHANGE = 0xc0
MIDI_CONTROL_CHANGE_FROM_CHRIS = 0x20 #Warning : this value is also received from voicelive...



count = 6;
for currentSong in SName:
  count+=1
  print ("\n##################")
  print ("Sending PC " + str(count))

  clientVideoPC.send_message("/video/obs", [OBS_COMMAND_SWITCH_SCENE, OBS_SCENE_DEFAULT])
  time.sleep(2) 
  clientVideoPC.send_message("/video/obs", [OBS_COMMAND_SWITCH_SCENE, OBS_SCENE_POWERPOINT])
  
	 
  clientVideoPC.send_message("/midi/voicelive", [MIDI_CONTROL_CHANGE, MIDI_CONTROL_CHANGE_FROM_CHRIS, 1])
  time.sleep(2)  	 

  
  clientVideoPC.send_message("/midi/voicelive", [MIDI_PROGRAM_CHANGE, count, 0])
  time.sleep(2)  
  clientVideoPC.send_message("/midi/voicelive", [MIDI_CONTROL_CHANGE, MIDI_CONTROL_CHANGE_FROM_CHRIS, 1])

  
  time.sleep(DELAY)

  clientVideoPC.send_message("/midi/voicelive", [MIDI_CONTROL_CHANGE, MIDI_CONTROL_CHANGE_FROM_CHRIS, 125])
  
  time.sleep(DELAY)

  clientVideoPC.send_message("/midi/voicelive", [MIDI_CONTROL_CHANGE, MIDI_CONTROL_CHANGE_FROM_CHRIS, 125])
 
  time.sleep(DELAY)

  clientVideoPC.send_message("/midi/voicelive", [MIDI_CONTROL_CHANGE, MIDI_CONTROL_CHANGE_FROM_CHRIS, 124])
  
  time.sleep(DELAY)

  clientVideoPC.send_message("/midi/voicelive", [MIDI_CONTROL_CHANGE, MIDI_CONTROL_CHANGE_FROM_CHRIS, 124])
 
  time.sleep(DELAY)

