"""Small example OSC server
This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

from GuitarAmpMidi import *
from SmoothDefines import *

MIDI_NOTE_OFF = 0x80
MIDI_NOTE_ON  = 0x90
MIDI_CONTROL_CHANGE = 0xb0
MIDI_PROGRAM_CHANGE = 0xc0

VL3_CC_GUITAR_UMOD 	= 21
VL3_CC_GUITAR_DELAY 	= 17
VL3_CC_GUITAR_REVERB 	= 46
VL3_CC_GUITAR_HIT 	= 47
VL3_CC_GUITAR_DRIVE 	= 29
VL3_CC_GUITAR_COMP 	= 19
VL3_CC_VOICE_UMOD 	= 118
VL3_CC_VOICE_DELAY 	= 117
VL3_CC_VOICE_REVERB 	= 112
VL3_CC_VOICE_HARMO 	= 110
VL3_CC_VOICE_DOUBLE 	= 111
VL3_CC_STEP 		= 115

currentSong = 0
currentStep = 0

#OSC connection to QLC+
clientQLC = udp_client.SimpleUDPClient("10.3.141.1", 5005)
#OSC connection to Mini PC
clientPC = udp_client.SimpleUDPClient("10.3.141.213", 5006)
#OSC connection to LaserHarp
clientLH = udp_client.SimpleUDPClient("10.3.141.90", 8001)





def SmoothTrioPC():
  global currentStep
  #TODO : implement on LH side
  clientLH.send_message("/laserharp/IDLE", 0)
   
  if(currentSong in SName):
    clientQLC.send_message("/stopallfunctions", 255)
    clientQLC.send_message("/stop", 255)
    clientQLC.send_message("/stop", 0)
    clientQLC.send_message("/stop", 255)
    clientQLC.send_message("/stop", 0)
    time.sleep(0.5)

    currentStep = 1
    currentMessage = "/start_cuelist/" + SName[currentSong]
    print("Sending OSC message to QLC : " + currentMessage)
    clientQLC.send_message(currentMessage, 255)
    time.sleep(0.5)
    clientQLC.send_message(currentMessage, 0)
  else:
    print("Smooth song unmapped. do nothing")
    #clientQLC.send_message("/stopallfunctions", 255)

    
    
def SmoothTrioCC(myCC, value):
  global currentStep
  #if step control
  #exlude first time step1, managed by Program Change. 
  #But allow to go back to it we already were beyond step1 
  tempNewStep = value + 1
  print ("myCC : " + str(myCC))
  if ((myCC == VL3_CC_STEP) and ((tempNewStep > 1) or (currentStep > 1))):
    previousStep = currentStep
    currentStep = tempNewStep
    
    if(currentSong in SName):
      #currentMessage = "/" + SName[currentSong] + "/Step" +str(currentStep)
      if (currentStep > previousStep):
        currentMessage = "/step_next"
      else:
        currentMessage = "/step_previous"  
	      
      print("Sending OSC message step to QLC : " + currentMessage)
      clientQLC.send_message(currentMessage, 255)
      clientQLC.send_message(currentMessage, 0)
    else:
      print("Step increment : Smooth song unmapped. do nothing")

  #Additional CC coming from Chris
  if (myCC == 20):
    currentMessage = "/step_next"
    clientQLC.send_message(currentMessage, 255)
    clientQLC.send_message(currentMessage, 0)
  #Additional CC coming from Chris
  if (myCC == 21):
    currentMessage = "/chris_talk"
    clientQLC.send_message(currentMessage, 255)
    clientQLC.send_message(currentMessage, 0)

 



def forwardPCFromVoicelive(myCC, value):
  global currentSong
  songName = ""
  currentSong = myCC + 1
  if(currentSong in SName):
    songName = SName[currentSong]
  print("Setting current song to : " + str(currentSong) + " (" + songName + ")")

    
  if(currentSong > SMOOTH_PRESET_MIN and currentSong < SMOOTH_PRESET_MAX):
    SmoothTrioPC()


#clientQLC.send_message("/fog", 255)
def forwardCCFromVoicelive(myCC, value):
  global clientQLC
  print("Dispatching message CC from Voicelive : " + str(myCC) + " | " + str(value))
  if(currentSong > SMOOTH_PRESET_MIN and currentSong < SMOOTH_PRESET_MAX):
    SmoothTrioCC(myCC, value)
  
  
  else:
    if   (myCC == VL3_CC_VOICE_HARMO):
      if (currentSong == 61):
        if(value > 0):
          clientQLC.send_message("/full_strobe", 255)
        else:
          clientQLC.send_message("/full_strobe", 0)

      else:      
        if (value > 0):
          clientQLC.send_message("/strobe", 255)
        else :
          clientQLC.send_message("/strobe", 0)

    if   (myCC == VL3_CC_GUITAR_UMOD):
      if (currentSong == 61):
        if(value > 0):
          clientQLC.send_message("/fog", 255)
        else:
          clientQLC.send_message("/fog", 0)

      else:      
        if (value > 0):
          setGMajorProgram(3)
          setAmpChannel(AMP_CHANNEL_CLEAN)
          clientQLC.send_message("/clean", 255)

    elif (myCC == VL3_CC_GUITAR_DELAY):
      if (currentSong == 61):
        clientQLC.send_message("/trip", 255)
      else:
        if (value > 0):
          setGMajorProgram(6)
          setAmpChannel(AMP_CHANNEL_BOOST)
          clientQLC.send_message("/boost", 255)
          print("Setting QLC boost")
    elif (myCC == VL3_CC_GUITAR_REVERB):
      if (value > 0):    
        setGMajorProgram(8)
        setAmpChannel(AMP_CHANNEL_XLEAD)
        clientQLC.send_message("/lead", 255)
    elif (myCC == VL3_CC_GUITAR_COMP):
      if (value > 0):
        setGMajorProgram(5)
        setAmpChannel(AMP_CHANNEL_CLEAN)
    elif (myCC == VL3_CC_GUITAR_DRIVE):
      if (value > 0):
        setGMajorDelay(1)
      else:
        setGMajorDelay(0)
    elif (myCC == VL3_CC_GUITAR_HIT):
      if(value > 0):
        setGMajorBoost(1)
        setGMajorDelay(1)
        clientQLC.send_message("/solo", 255)
      else:
        setGMajorBoost(0)
        setGMajorDelay(0)
        clientQLC.send_message("/solo", 0)
    else:
      print("message unmapped. do nothing")


def print_voicelive_handler(unused_addr, args, command, note, vel):
  
  if(command == MIDI_NOTE_ON):
    print("MIDI_NOTE_ON")
  if(command == MIDI_NOTE_OFF):
    print("MIDI_NOTE_OFF")  
  if(command == MIDI_CONTROL_CHANGE):
    print("MIDI_CONTROL_CHANGE")
    forwardCCFromVoicelive(note, vel)
  if(command == MIDI_PROGRAM_CHANGE):
    print("MIDI_PROGRAM_CHANGE")
    forwardPCFromVoicelive(note, vel)

    
  print("[{0}] ~ {1} {2} {3}\n".format(args[0], command, note, vel))
   

def print_laserharp_handler(osc_address, args, command):
  print ("Received OSC message from Laser Harp")
  print("address" + osc_address)
  print(command);
  clientPC.send_message(osc_address, command);
  
  #print("[{0}] ~ {1} {2} {3}\n".format(args[0], command, note, vel))
   

def print_note_handler(unused_addr, args, arg2, note):
  print("[{0}] ~ {1} {2}".format(args[0], arg2, note))
  
def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

if __name__ == "__main__":

 # while(1):
 #   print("sending LH preset to Laserharp")
 #   clientLH.send_message("/laserharp/startLH", 2)
 #   time.sleep(2)
 #   print("sending DMX request to Laserharp")
 #   clientLH.send_message("/laserharp/startDMX", 0)
 #   time.sleep(2)
      
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="10.3.141.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=8000, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/midi/voicelive", print_voicelive_handler, "Midi_voicelive")
  dispatcher.map("/vkb_midi/0/*", print_laserharp_handler, "Midi_laserharp")

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  
  

  
  server.serve_forever()
