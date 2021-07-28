
from SmoothDefines import *  #TODO : used only for OBS. not smooth specific

DMX_CHANNEL_LH_CONTROL = 16
LH_CONTROL_IDLE = 1
LH_CONTROL_DMX  = 2
LH_CONTROL_LH_PRESET_OFFSET  = 3

DMX_CHANNEL_MEGASCREEN_BASE 	= 24
DMX_MEGASCREEN_ALPHA 		= DMX_CHANNEL_MEGASCREEN_BASE
DMX_MEGASCREEN_RED 		= DMX_CHANNEL_MEGASCREEN_BASE + 1
DMX_MEGASCREEN_GREEN		= DMX_CHANNEL_MEGASCREEN_BASE + 2
DMX_MEGASCREEN_BLUE		= DMX_CHANNEL_MEGASCREEN_BASE + 3
DMX_MEGASCREEN_STROBE		= DMX_CHANNEL_MEGASCREEN_BASE + 4

DMX_CHANNEL_VISUALIZER_BASE 	= 32
DMX_CHANNEL_VISUALIZER_PRESET 	= DMX_CHANNEL_VISUALIZER_BASE
DMX_CHANNEL_VISUALIZER_LOCK 	= DMX_CHANNEL_VISUALIZER_BASE + 1
DMX_CHANNEL_VISUALIZER_RANDOM 	= DMX_CHANNEL_VISUALIZER_BASE + 2

DMX_CHANNEL_OBS_BASE 		= 20
DMX_CHANNEL_OBS_COLLECTION 	= DMX_CHANNEL_OBS_BASE
DMX_CHANNEL_OBS_SCENE 		= DMX_CHANNEL_OBS_BASE + 1

DEBOUNCE_DELAY = 0.3
DELAY_TO_SEND_LAST_VALUES = 0.6


def process_OSC_2_video_PC(clientVideoPC, channel, value):
    print("process_OSC_2_video_PC : ", channel, value)
    if(int(channel) == DMX_CHANNEL_VISUALIZER_PRESET - 1):
      print("Received VideoPC Visualizer preset OSC change")
      clientVideoPC.send_message("/video/visualizer/preset", value)
      return

    if(int(channel) == DMX_CHANNEL_VISUALIZER_LOCK - 1):
      print("Received VideoPC Visualizer command OSC change")
      clientVideoPC.send_message("/video/visualizer/lock", value)
      return

    if(int(channel) == DMX_CHANNEL_VISUALIZER_RANDOM - 1):
      print("Received VideoPC Visualizer command OSC change")
      clientVideoPC.send_message("/video/visualizer/random", value)
      return
                  
    if(int(channel) == DMX_CHANNEL_OBS_SCENE - 1):
      print("Received VideoPC OBS Scene OSC Command")
      clientVideoPC.send_message("/video/obs", [OBS_COMMAND_SWITCH_SCENE, value])
      return
      
    if(int(channel) == DMX_CHANNEL_OBS_COLLECTION - 1):
      print("Received VideoPC OBS COllection OSC Command")
      clientVideoPC.send_message("/video/obs", [OBS_COMMAND_SWITCH_COLLECTION, value])
      return
  
