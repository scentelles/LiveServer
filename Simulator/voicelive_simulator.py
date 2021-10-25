import sys
sys.path.append("..")  
from SmoothDefines import *
import time
from pythonosc import udp_client

from prompt_toolkit import prompt

import socket 



#sendosc 10.3.141.1 5005 /step_next i 255

#OSC connection to QLC+



   
if(len(sys.argv) > 1):
    hostname = socket.gethostname()
    liveserver_ip = socket.gethostbyname(hostname)
else:
    liveserver_ip = "10.3.141.1"

print(liveserver_ip)
clientQLC = udp_client.SimpleUDPClient(liveserver_ip, 8000)

#First set a progam change corresponding to Smooth range
#clientQLC.send_message("/midi/voicelive", [MIDI_PROGRAM_CHANGE, SMOOTH_PRESET_ANOTHER_TOWN, 0])
#
#time.sleep(2)
index = 0
choice2song = [0 for i in range(len(SName)+1)]
for song_id in SName.keys():
    index += 1
    print("(" + str(index) + ") " + "preset " + str(song_id) + " \t: " +  SName[song_id])
    choice2song[index] = song_id
print("> : Next Step")
print("< : Previous Step")
print("* : Chris Talk")    
print("+ : Shutdown")

while (True):
    choice = prompt('Make your choice: ')
    print('You chose: %s' % choice)
    if(choice == ">"):
        print ("Next Step in QLC...")
        clientQLC.send_message("/midi/voicelive", [MIDI_CONTROL_CHANGE, MIDI_CONTROL_CHANGE_FROM_CHRIS, MIDI_CC_CHRIS_NEXT_STEP])
    elif(choice == "<"):
        print ("Previous Step in QLC...")
        clientQLC.send_message("/midi/voicelive", [MIDI_CONTROL_CHANGE, MIDI_CONTROL_CHANGE_FROM_CHRIS, MIDI_CC_CHRIS_PREVIOUS_STEP])
    elif(choice == "*"): 
        print ("Chris talk in QLC...")
        clientQLC.send_message("/midi/voicelive", [MIDI_CONTROL_CHANGE, MIDI_CONTROL_CHANGE_FROM_CHRIS, MIDI_CC_CHRIS_TALK])    
    elif(choice == "+"): 
        print ("sending shutdown...")
        clientQLC.send_message("/midi/shutdown", 1)    
    else:
        print ("Selecting Song In QLC : ", SName[choice2song[int(choice)]])
        clientQLC.send_message("/midi/voicelive", [MIDI_PROGRAM_CHANGE, choice2song[int(choice)]-1, 0])
   