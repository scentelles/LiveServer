
from SmoothDefines import *  #TODO : used only for OBS. not smooth specific

DMX_CHANNEL_VISUALIZER_BASE 	= 32
DMX_CHANNEL_VISUALIZER_PRESET 	= DMX_CHANNEL_VISUALIZER_BASE
DMX_CHANNEL_VISUALIZER_LOCK 	= DMX_CHANNEL_VISUALIZER_BASE + 1
DMX_CHANNEL_VISUALIZER_RANDOM 	= DMX_CHANNEL_VISUALIZER_BASE + 2

DMX_CHANNEL_OBS_BASE 		= 20
DMX_CHANNEL_OBS_COLLECTION 	= DMX_CHANNEL_OBS_BASE
DMX_CHANNEL_OBS_SCENE 		= DMX_CHANNEL_OBS_BASE + 1

DMX_CHANNEL_SLIDESSHOW_CONTROL = 22


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
      
    if(int(channel) == DMX_CHANNEL_SLIDESSHOW_CONTROL - 1):
      print("Received VideoPC Slideshow OSC Command")
      clientVideoPC.send_message("/video/slideshow", value)
      time.sleep(0.5)
      #get back to 0 to trigger change if consecutive same commands are set
      clientVideoPC.send_message("/video/slideshow", 0)
      return  
