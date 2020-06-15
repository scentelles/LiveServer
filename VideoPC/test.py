import sys  
sys.path.append("..")  

from SmoothDefines import *
import time
from pythonosc import udp_client

#OSC connection to Video manager
#LOCALHOST_IP   = "192.168.1.51"
LOCALHOST_IP   = "192.168.1.22"
LOCALHOST_PORT = 5007
clientVideoPC = udp_client.SimpleUDPClient(LOCALHOST_IP, LOCALHOST_PORT)

DELAY = 1

MIDI_CONTROL_CHANGE = 0xb0
MIDI_PROGRAM_CHANGE = 0xc0

def testProjectMControl():
	print ("\n\nTEST : PROJECTM control\n")  
	clientVideoPC.send_message("/video/projectm/command", [2,1]) #random enable command
	time.sleep(5)
	clientVideoPC.send_message("/video/projectm/command", [1,1]) #lock command
	time.sleep(5)
	clientVideoPC.send_message("/video/projectm/command", [2,0]) #random disable command
	time.sleep(5)
	clientVideoPC.send_message("/video/projectm/command", [1,0]) #unlock command
	time.sleep(20)

		
	clientVideoPC.send_message("/video/projectm/preset", 5)
	time.sleep(5)
	clientVideoPC.send_message("/video/projectm/preset", 10)
	time.sleep(5)
	clientVideoPC.send_message("/video/projectm/preset", 100)

	
def testOBSControl():
	print ("\n\nTEST : OBS control\n")  
	clientVideoPC.send_message("/video/obs", [OBS_COMMAND_SWITCH_SCENE, OBS_SCENE_DEFAULT])
	time.sleep(2) 
	clientVideoPC.send_message("/video/obs", [OBS_COMMAND_SWITCH_SCENE, OBS_SCENE_POWERPOINT])
	time.sleep(2) 
	#TBD


	
def testPresetSlideshowSwitch():
	print ("\n\nTEST : Slideshow switch\n")
	count = 6; #start at index 6. other presets are not used in voicelive
	for currentSong in SName:
	  count+=1
	  print ("\n##################")
	  print ("Sending PC " + str(count))

	  #=====================================
	  #test changing preset during Christalk 
	  #entering Chris talk
	  clientVideoPC.send_message("/midi/voicelive", [MIDI_CONTROL_CHANGE, MIDI_CONTROL_CHANGE_FROM_CHRIS, MIDI_CC_CHRIS_TALK])
	  time.sleep(2)  	 

	  #sending program change
	  clientVideoPC.send_message("/midi/voicelive", [MIDI_PROGRAM_CHANGE, count, 0])
	  time.sleep(2)  
	  
	  #exiting Chris talk
	  clientVideoPC.send_message("/midi/voicelive", [MIDI_CONTROL_CHANGE, MIDI_CONTROL_CHANGE_FROM_CHRIS, MIDI_CC_CHRIS_TALK])
	  time.sleep(DELAY)

	  #Now we can send next/previous slide commands
	  clientVideoPC.send_message("/midi/voicelive", [MIDI_CONTROL_CHANGE, MIDI_CONTROL_CHANGE_FROM_CHRIS, MIDI_CC_CHRIS_NEXT_SLIDE])
	  time.sleep(DELAY)

	  clientVideoPC.send_message("/midi/voicelive", [MIDI_CONTROL_CHANGE, MIDI_CONTROL_CHANGE_FROM_CHRIS, MIDI_CC_CHRIS_NEXT_SLIDE])
	  time.sleep(DELAY)

	  clientVideoPC.send_message("/midi/voicelive", [MIDI_CONTROL_CHANGE, MIDI_CONTROL_CHANGE_FROM_CHRIS, MIDI_CC_CHRIS_PREVIOUS_SLIDE])
	  time.sleep(DELAY)

	  clientVideoPC.send_message("/midi/voicelive", [MIDI_CONTROL_CHANGE, MIDI_CONTROL_CHANGE_FROM_CHRIS, MIDI_CC_CHRIS_PREVIOUS_SLIDE])
	  time.sleep(DELAY)
	  
testProjectMControl()
testOBSControl()
testPresetSlideshowSwitch()
