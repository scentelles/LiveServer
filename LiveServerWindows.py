"""Small example OSC server
This program listens to several addresses, and prints some information about
received packets.
"""
import sys 
import os
import argparse
import math
import socket 

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
chrisTalkOngoing = 0


fogOngoing = 0



def startCueList(songId):
    global currentStep
    
    clientQLC.send_message("/stopallfunctions", 255)
    clientQLC.send_message("/stop", 255)
    clientQLC.send_message("/stop", 0)
    clientQLC.send_message("/stop", 255)
    clientQLC.send_message("/stop", 0)
    time.sleep(0.5)

    currentStep = 1
    currentMessage = "/start_cuelist/" + SName[songId]
    print("Sending OSC message to QLC : " + currentMessage)
    clientQLC.send_message(currentMessage, 255)
    time.sleep(0.5)
    clientQLC.send_message(currentMessage, 0)

def startSong(songId):
    clientVideoPC.send_message("/video/song", songId) #TODO : check currentsong key exists

    startCueList(songId)


def SmoothTrioPC():
  global currentStep
  global currentSong

  
  if((currentSong in SName) and (chrisTalkOngoing == 0)):  
    startSong(currentSong)

  else:
    print("Smooth song unmapped or Christalk ongoing. do nothing")
    #clientQLC.send_message("/stopallfunctions", 255)

    
    
def SmoothTrioCC(myCC, value):
  global currentStep
  global chrisTalkOngoing
  global currentSong
  
  #if step control
  #exlude first time step1, managed by Program Change. 
  #But allow to go back to it we already were beyond step1 
  tempNewStep = value + 1
  print ("myCC : " + str(myCC))
  
  
    
  
  
  if (myCC == VL3_CC_STEP):
   #Upon Step2, (generally the start of the song, no Christalk is allowed.
   #Forcing Christalk deactivation and resetting to current song start
   if(tempNewStep == 2):
     chrisTalkOngoing = 0
     startSong(currentSong) #contains a stop all function call, should be sufficient to stop the chris talk
     time.sleep(0.1) 

   if ((tempNewStep > 1) or (currentStep > 1)) and (chrisTalkOngoing == 0):
      previousStep = currentStep
      currentStep = tempNewStep

      if(currentSong in SName):


	#Special case of going from last to first step on voicelive.
	#Using it to reset to step1, stop all functiona and restart cue
	#will work only for presets with more than2 steps...
        if(abs(previousStep - currentStep) > 1):
            print("resetting Cue and restart")
            startSong(currentSong)
            return

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
  if (myCC == MIDI_CONTROL_CHANGE_FROM_CHRIS) : 
    if(value == MIDI_CC_CHRIS_NEXT_STEP):
       print("From Chris : next step")
       currentMessage = "/step_next"
       currentStep = currentStep + 1
       clientQLC.send_message(currentMessage, 255)
       clientQLC.send_message(currentMessage, 0)
    elif(value == MIDI_CC_CHRIS_PREVIOUS_STEP):
       print("From Chris : previous step")
       currentStep = currentStep - 1
       currentMessage = "/step_previous"  
       clientQLC.send_message(currentMessage, 255)
       clientQLC.send_message(currentMessage, 0)       
    elif(value == MIDI_CC_CHRIS_NEXT_SLIDE):
       print("From Chris : next slide")
       clientVideoPC.send_message("/video/slideshow", SLIDESHOW_COMMAND_NEXT_SLIDE)
    elif(value == MIDI_CC_CHRIS_PREVIOUS_SLIDE):
       print("From Chris : previous slide")
       clientVideoPC.send_message("/video/slideshow", SLIDESHOW_COMMAND_NEXT_SLIDE)

    elif(value == MIDI_CC_CHRIS_TALK):
       print("Setting Chris Talk Scene")

       if(chrisTalkOngoing == 0):
           chrisTalkOngoing = 1
	   
           clientVideoPC.send_message("/video/song", SMOOTH_PRESET_CHRIS_TALK) 

           clientQLC.send_message("/stopallfunctions", 255) 
           clientQLC.send_message("/stop", 255)
           clientQLC.send_message("/stop", 0)
           clientQLC.send_message("/stop", 255)
           clientQLC.send_message("/stop", 0)
           time.sleep(0.5)
           currentMessage = "/chris_talk"	      
           clientQLC.send_message(currentMessage, 255)
           clientQLC.send_message(currentMessage, 0)

       else:  #restart cue list of current song when going out of CHris talk
           chrisTalkOngoing = 0
           startSong(currentSong) #contains a stop all function call, should be sufficient to stop the chris talk


  else:
       print("Message from Chris unrecognized")




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
          #when going out of solo, or strobe, go back to boost
          time.sleep(0.1)
          clientQLC.send_message("/boost", 255)

      else:      
        if (value > 0):
          clientQLC.send_message("/strobe", 255)
        else :
          clientQLC.send_message("/strobe", 0)
          #when going out of solo, or strobe, go back to boost
          time.sleep(0.1)
          clientQLC.send_message("/boost", 255)

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
        time.sleep(0.1)
        clientQLC.send_message("/solo", 0)
      else:
        setGMajorBoost(0)
        setGMajorDelay(0)
        clientQLC.send_message("/solo", 255)
        time.sleep(0.1)
        clientQLC.send_message("/solo", 0)
    else:
      print("message unmapped. do nothing - Did you at least set a song preset?")


def print_voicelive_handler(unused_addr, args, command, note, vel):
  
  if(command == MIDI_NOTE_ON):
    print("MIDI_NOTE_ON")
  if(command == MIDI_NOTE_OFF):
    print("MIDI_NOTE_OFF")  
  if(command == MIDI_CONTROL_CHANGE):
    print("MIDI_CONTROL_CHANGE")
    forwardCCFromVoicelive(note, vel)
#  if(command == MIDI_CONTROL_CHANGE_FROM_CHRIS)://nolonger needed
#    print("MIDI_CONTROL_CHANGE_FROM_CHRIS")
#    forwardCCFromChris(note, vel)
  if(command == MIDI_PROGRAM_CHANGE):
    print("MIDI_PROGRAM_CHANGE")
    forwardPCFromVoicelive(note, vel)

    
  print("\n[{0}] ~ {1} {2} {3}".format(args[0], command, note, vel))
   

def print_switch_handler(unused_addr, args, switchId, value):
  
  global fogOngoing 
  global currentStep
  print("\nReceive Switch OSC message : [{0}] ~ {1} {2} ".format(args[0], switchId, value))
  if(switchId == 3):
    if(value > 0):
      if(fogOngoing == 0):
        print("Switching fog On")
        clientQLC.send_message("/fog", 255)
        fogOngoing = 1
      else:
        print("Switching fog Off")
        clientQLC.send_message("/fog", 0)
        fogOngoing = 0
	
  if(switchId == 1):
    if(value > 0):
       print("From Switch : next step")
       currentMessage = "/step_next"
       currentStep = currentStep + 1
       clientQLC.send_message(currentMessage, 255)
       clientQLC.send_message(currentMessage, 0)

def print_shutdown_handler(unused_addr, args, value):
  print("Shutting down Megascreen")
  clientMS.send_message("/MS/shutdown", 1) 
  print("Shutting down system")
  os.system("shutdown -h -P now")  


def print_note_handler(unused_addr, args, arg2, note):
  print("[{0}] ~ {1} {2}".format(args[0], arg2, note))
  
def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

if __name__ == "__main__":


  print ("Argument nb:", len(sys.argv))


  local_ip = "10.3.141.3"
  videoPC_ip = "10.3.141.3"
  
  print("local IP : ", local_ip)
  
  
  #OSC connection to QLC+
  clientQLC = udp_client.SimpleUDPClient(local_ip, 5005)
  #OSC connection to Mini PC
  clientPC = udp_client.SimpleUDPClient(videoPC_ip, 5006)
  #OSC connection to Video PC
  clientVideoPC = udp_client.SimpleUDPClient(videoPC_ip, 5007)
  #OSC connection to Megascreen - used only to shutdown
  clientMS = udp_client.SimpleUDPClient("10.3.141.5", 7702)


  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/midi/voicelive", print_voicelive_handler, "Midi_voicelive OSC")
  dispatcher.map("/midi/shutdown", print_shutdown_handler, "Shutdown")
  dispatcher.map("/switch", print_switch_handler, "Switch OSC")

  server = osc_server.ThreadingOSCUDPServer(
      (local_ip, 8000), dispatcher)
  print("Serving on {}".format(server.server_address))
  
  

  
  server.serve_forever()
