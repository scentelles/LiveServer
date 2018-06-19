"""Small example OSC server
This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server

MIDI_NOTE_OFF = 0x80
MIDI_NOTE_ON  = 0x90
MIDI_CONTROL_CHANGE = 0xb0
MIDI_PROGRAM_CHANGE = 0xc0

def print_midi_handler(unused_addr, args, command, note, vel):
  if(command == MIDI_NOTE_ON):
    print("MIDI_NOTE_ON")
  if(command == MIDI_NOTE_OFF):
    print("MIDI_NOTE_OFF")  
  if(command == MIDI_CONTROL_CHANGE):
    print("MIDI_CONTROL_CHANGE")
  if(command == MIDI_PROGRAM_CHANGE):
    print("MIDI_PROGRAM_CHANGE")
          
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
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=8000, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  #dispatcher.map("/filter", print)
  #dispatcher.map("/volume", print_volume_handler, "Volume")
  dispatcher.map("/midi/voicelive", print_midi_handler, "Midi")
  #dispatcher.map("/channel/0/note/*", print_note_handler, "Note")
  #dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()
