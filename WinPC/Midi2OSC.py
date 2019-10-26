"""Show how to receive MIDI input by setting a callback function."""

from __future__ import print_function

import logging
import sys
import time

import rtmidi
from rtmidi.midiutil import open_midiinput

from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc import dispatcher

import os

RASPI_IP = "10.3.141.1"
LOCALHOST_IP = "10.3.141.213"

midiout = rtmidi.MidiOut()
midiout.open_port(5)

log = logging.getLogger('midiin_callback')
logging.basicConfig(level=logging.DEBUG)


class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        #Only change program change
        if(message[0] == 0xC0):
           #send program change thru OSC
           client.send_message("/midi/voicelive", [message[0], message[1], 0])
           if(message[1] == 1): #We don't receive the preset 1(index 0...), so let's use the number 2(index 1).
              #shutdown
              print("Shuting down immediately")
              cmd = "Shutdown -s -f -t 0"
              os.system(cmd)
 
        else:
           #send Control change thru OSC
           client.send_message("/midi/voicelive", [message[0], message[1], message[2]])
       

#Receives note on and off coming from LaserHarp
def print_laserharp_handler(osc_address, args, command):
  print("received OSC message from laser harp")
  print("adress" + osc_address)
  print(command)

  temp = osc_address.split("/")
  print (temp[4]);
  if(command != 0):
    note = [0x90, int(temp[4]), command]    # Note ON
  else:
    note = [0x80, int(temp[4]), 0]          #note OFF
  midiout.send_message(note)
 

client = udp_client.SimpleUDPClient(RASPI_IP, 8000)

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/vkb_midi/0/*", print_laserharp_handler, "midi_laserharp")

server = osc_server.ThreadingOSCUDPServer(
    (LOCALHOST_IP, 5006), dispatcher)
# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
#port = sys.argv[1] if len(sys.argv) > 1 else None

try:
   midiin, port_name = open_midiinput(3) #vMidi2
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler(port_name))

print("Entering main loop. Press Control-C to exit.")


server.serve_forever()
    

