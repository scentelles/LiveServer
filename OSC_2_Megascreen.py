
from SmoothDefines import *  #TODO : used only for OBS. not smooth specific

DMX_CHANNEL_MEGASCREEN_BASE 	= 24
DMX_MEGASCREEN_ALPHA 		= DMX_CHANNEL_MEGASCREEN_BASE
DMX_MEGASCREEN_RED 		= DMX_CHANNEL_MEGASCREEN_BASE + 1
DMX_MEGASCREEN_GREEN		= DMX_CHANNEL_MEGASCREEN_BASE + 2
DMX_MEGASCREEN_BLUE		= DMX_CHANNEL_MEGASCREEN_BASE + 3
DMX_MEGASCREEN_STROBE		= DMX_CHANNEL_MEGASCREEN_BASE + 4



def process_OSC_2_MegaScreen(clientMS, channel, value):
    print("process_OSC_2_MegaScreen : ", channel, value)
    if(int(channel) == DMX_MEGASCREEN_ALPHA - 1):
      print("Received Megascreen Alpha OSC change")
      clientMS.send_message("/MS/alpha", value)
      return

    if(int(channel) == DMX_MEGASCREEN_RED - 1):
      print("Received Megascreen Red OSC change")
      clientMS.send_message("/MS/red", value)
      return

    if(int(channel) == DMX_MEGASCREEN_GREEN - 1):
      print("Received Megascreen Green OSC change")
      clientMS.send_message("/MS/green", value)
      return
      
    if(int(channel) == DMX_MEGASCREEN_BLUE - 1):
      print("Received Megascreen Blue OSC change")
      clientMS.send_message("/MS/blue", value)
      return
      
    if(int(channel) == DMX_MEGASCREEN_STROBE - 1):
      print("Received Megascreen Strobe OSC change")
      clientMS.send_message("/MS/strobe", value)
      return  
