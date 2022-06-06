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

from GuitarAmpMidi   import *
from SmoothDefines   import *
from RedCloudDefines import *

import threading


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

    startCueList(songId)


  

def forwardPCFromVoicelive(myCC, value):
  global currentSong
  songName = ""
  currentSong = myCC + 1
  if(currentSong in SName):
    songName = SName[currentSong]
  print("Setting current song to : " + str(currentSong) + " (" + songName + ")")

    
  if(currentSong > SMOOTH_PRESET_MIN and currentSong < SMOOTH_PRESET_MAX):
    print("On RASPI, do nothing when in Smooth trio config")


#clientQLC.send_message("/fog", 255)
def forwardCCFromVoicelive(myCC, value):
  global clientQLC
  print("Dispatching message CC from Voicelive : " + str(myCC) + " | " + str(value))
  if(currentSong > SMOOTH_PRESET_MIN and currentSong < SMOOTH_PRESET_MAX):
    print("On RASPI, do nothing when in Smooth trio config")
  
  
  else:
    if   (myCC == VL3_CC_VOICE_HARMO):
      if (currentSong == RED_CLOUD_LIGHT_PROGRAM):
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
      if (currentSong == RED_CLOUD_LIGHT_PROGRAM):
        print("LIGHTING")
        if(value > 0):
          clientQLC.send_message("/fog", 255)
        else:
          clientQLC.send_message("/fog", 0)

      else:      
        if (value > 0):
          setGMajorProgram(midi_output, 3)
          setAmpChannel(midi_output, AMP_CHANNEL_CLEAN)
          clientQLC.send_message("/clean", 255)

    elif (myCC == VL3_CC_GUITAR_DELAY):
      if (currentSong == RED_CLOUD_LIGHT_PROGRAM):
        clientQLC.send_message("/trip", 255)
      else:
        if (value > 0):
          setGMajorProgram(midi_output, 6)
          setAmpChannel(midi_output, AMP_CHANNEL_BOOST)
          clientQLC.send_message("/boost", 255)
          print("Setting QLC boost")
    elif (myCC == VL3_CC_GUITAR_REVERB):
      if (value > 0):    
        setGMajorProgram(midi_output, 8)
        setAmpChannel(midi_output, AMP_CHANNEL_XLEAD)
        clientQLC.send_message("/lead", 255)
    elif (myCC == VL3_CC_GUITAR_COMP):
      if (value > 0):
        setGMajorProgram(midi_output, 5)
        setAmpChannel(midi_output, AMP_CHANNEL_CLEAN)
    elif (myCC == VL3_CC_GUITAR_DRIVE):
      if (value > 0):
        setGMajorDelay(midi_output, 1)
      else:
        setGMajorDelay(midi_output, 0)
    elif (myCC == VL3_CC_GUITAR_HIT):
      if(value > 0):
        setGMajorBoost(midi_output, 1)
        setGMajorDelay(midi_output, 1)
        clientQLC.send_message("/solo", 255)
        time.sleep(0.1)
        clientQLC.send_message("/solo", 0)
      else:
        setGMajorBoost(midi_output, 0)
        setGMajorDelay(midi_output, 0)
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
   
def print_shutdown_handler(unused_addr, args, value):
  print("Shutting down system")
  os.system("shutdown -h -P now")  


def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

def midiReceiveThread(name):
    while (1):
      msg = midi_input.receive()
      print (msg)
      if(msg.type == 'program_change'):
        print("MIDI_PROGRAM_CHANGE")
        forwardPCFromVoicelive(msg.program, 0)
      elif(msg.type == 'control_change'):
        forwardCCFromVoicelive(msg.control, msg.value)
       
      print("looping")
      time.sleep(0.1)


if __name__ == "__main__":


  local_ip = "10.3.141.2"
  videoPC_ip = "10.3.141.2"
  
  print("local IP : ", local_ip)
  
  
  #OSC connection to QLC+
  clientQLC = udp_client.SimpleUDPClient(local_ip, 5005)

  x = threading.Thread(target=midiReceiveThread, args=(1,))
  x.start()


  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/midi/voicelive", print_voicelive_handler, "Midi_voicelive OSC")
  dispatcher.map("/midi/shutdown", print_shutdown_handler, "Shutdown")

  server = osc_server.ThreadingOSCUDPServer(
      (local_ip, 8000), dispatcher)
  print("Serving on {}".format(server.server_address))
  
  

  
  server.serve_forever()
