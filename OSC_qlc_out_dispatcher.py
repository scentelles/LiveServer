#!/usr/bin/env python3

import time
import threading
import sys
import socket 
from threading import Timer

from OSC_2_video_PC import * 
from OSC_2_Megascreen import * 

from pythonosc import osc_server
from pythonosc import dispatcher

from pythonosc import udp_client

from SmoothDefines import *  #TODO : used only for OBS. not smooth specific

print ("Argument nb:", len(sys.argv))

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
videoPC_ip = local_ip


OSC_ADDRESS   = "127.0.0.1"
OSC_PORT      = 9002         #corresponds to universe #3

DMX_CHANNEL_LH_CONTROL = 16
LH_CONTROL_IDLE = 1
LH_CONTROL_DMX  = 2
LH_CONTROL_LH_PRESET_OFFSET  = 3


DEBOUNCE_DELAY = 0.3
DELAY_TO_SEND_LAST_VALUES = 0.6


clientLH = udp_client.SimpleUDPClient("10.3.141.90", 8001)
clientMS = udp_client.SimpleUDPClient("10.3.141.133", 7701)
#OSC connection to Video PC
clientVideoPC = udp_client.SimpleUDPClient(videoPC_ip, 5007)

def dispatch_qlc_osc_handler(osc_address, args, command):

  global ledThreads
  global clientLH

  channel = (osc_address.split("/"))[3]
  ledIndex = int(int(channel)/3)
  channelIndex = int(channel)%3
  value = round(command*255)


  if(int(channel) == DMX_CHANNEL_LH_CONTROL - 1):
    print("Received LH OSC Command")

    if(value == LH_CONTROL_IDLE):
      print("LH : Setting LH in IDLE mode")
      clientLH.send_message("/laserharp/startIDLE", 0)
    if(value == LH_CONTROL_DMX):
      print("LH : Settinh LH in DMX mode")
      clientLH.send_message("/laserharp/startDMX", 0)
    if(value >= LH_CONTROL_LH_PRESET_OFFSET):
      preset = value - LH_CONTROL_LH_PRESET_OFFSET
      print("LH : Setting LH mode, preset : " + str(preset))
      clientLH.send_message("/laserharp/startLH", preset)      #To be tested
    return

  process_OSC_2_MegaScreen(clientMS, channel, value)

  process_OSC_2_video_PC(clientVideoPC, channel, value)
  


dispatcher = dispatcher.Dispatcher()
dispatcher.map("/*", dispatch_qlc_osc_handler, "QLC")

server = osc_server.ThreadingOSCUDPServer((OSC_ADDRESS, OSC_PORT), dispatcher)
print("Serving on {}".format(server.server_address))


server.serve_forever()


     


