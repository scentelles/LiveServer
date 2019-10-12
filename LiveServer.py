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

MIDI_NOTE_OFF = 0x80
MIDI_NOTE_ON  = 0x90
MIDI_CONTROL_CHANGE = 0xb0
MIDI_PROGRAM_CHANGE = 0xc0

VL3_CC_GUITAR_UMOD = 21
VL3_CC_GUITAR_DELAY = 17
VL3_CC_GUITAR_REVERB = 46
VL3_CC_GUITAR_HIT = 47
VL3_CC_GUITAR_DRIVE = 29
VL3_CC_GUITAR_COMP = 19
VL3_CC_VOICE_UMOD = 118
VL3_CC_VOICE_DELAY = 117
VL3_CC_VOICE_REVERB = 112
VL3_CC_VOICE_HARMO = 110
VL3_CC_VOICE_DOUBLE = 111

currentSong = 0
currentStep = 1

#OSC connection to QLC+
client = udp_client.SimpleUDPClient("10.3.141.1", 5005)


SMOOTH_PRESET_ANOTHER_TOWN		= 0
SMOOTH_PRESET_NIGHT_SHADOW_TRAIN 	= 0
SMOOTH_PRESET_L_AVERSE 			= 0
SMOOTH_PRESET_DARKNESS_OF_YOUR_EYES	= 0
SMOOTH_PRESET_LE_BAL 			= 0
SMOOTH_PRESET_SLAP_MY_HEAD		= 0
SMOOTH_PRESET_AFTER_CHRISTMAS		= 0
SMOOTH_PRESET_BOIPEBA			= 0
SMOOTH_PRESET_BOIPEBA			= 0
SMOOTH_PRESET_BOIPEBA			= 0
SMOOTH_PRESET_BOIPEBA			= 0
SMOOTH_PRESET_BOIPEBA			= 0

SMOOTH_PRESET_MIN = 1
SMOOTH_PRESET_MAX = 49


def SmoothTrioCC():
  if(currentSong == SMOOTH_PRESET_ANOTHER_TOWN):
    #if step control
    currentStep += 1
    
    client.send_message("/AnotherTown/" + currentStep, 255)

  
  else:
    print("Smooth message unmapped. do nothing")




#client.send_message("/fog", 255)
def forwardCCFromVoicelive(myCC, value):
  global client

  if(currentSong > SMOOTH_PRESET_MIN and currentSong < SMOOTH_PRESET_MAX):
    SmoothTrioCC()
  
  
  else:
    if   (myCC == VL3_CC_VOICE_HARMO):
      if (currentSong == 61):
        if(value > 0):
          client.send_message("/full_strobe", 255)
        else:
          client.send_message("/full_strobe", 0)

      else:      
        if (value > 0):
          client.send_message("/strobe", 255)
        else :
          client.send_message("/strobe", 0)

    if   (myCC == VL3_CC_GUITAR_UMOD):
      if (currentSong == 61):
        if(value > 0):
          client.send_message("/fog", 255)
        else:
          client.send_message("/fog", 0)

      else:      
        if (value > 0):
          setGMajorProgram(3)
          setAmpChannel(AMP_CHANNEL_CLEAN)
          client.send_message("/clean", 255)

    elif (myCC == VL3_CC_GUITAR_DELAY):
      if (currentSong == 61):
        client.send_message("/trip", 255)
      else:
        if (value > 0):
          setGMajorProgram(6)
          setAmpChannel(AMP_CHANNEL_BOOST)
          client.send_message("/boost", 255)
    elif (myCC == VL3_CC_GUITAR_REVERB):
      if (value > 0):    
        setGMajorProgram(8)
        setAmpChannel(AMP_CHANNEL_XLEAD)
        client.send_message("/lead", 255)
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
        client.send_message("/solo", 255)
      else:
        setGMajorBoost(0)
        setGMajorDelay(0)
        client.send_message("/solo", 0)
    else:
      print("message unmapped. do nothing")


def print_midi_handler(unused_addr, args, command, note, vel):
  global currentSong
  
  if(command == MIDI_NOTE_ON):
    print("MIDI_NOTE_ON")
  if(command == MIDI_NOTE_OFF):
    print("MIDI_NOTE_OFF")  
  if(command == MIDI_CONTROL_CHANGE):
    print("MIDI_CONTROL_CHANGE")
    forwardCCFromVoicelive(note, vel)
  if(command == MIDI_PROGRAM_CHANGE):
    print("MIDI_PROGRAM_CHANGE")
    print("Setting current song to : ")
    print(note+1)
    currentSong = note + 1  
    
  print("[{0}] ~ {1} {2} {3}\n".format(args[0], command, note, vel))
   

def print_note_handler(unused_addr, args, arg2, note):
  print("[{0}] ~ {1} {2}".format(args[0], arg2, note))
  
def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="10.3.141.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=8000, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/midi/voicelive", print_midi_handler, "Midi")

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  
  

  
  server.serve_forever()
