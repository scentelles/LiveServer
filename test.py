from SmoothDefines import *
import time
from pythonosc import udp_client

#sendosc 10.3.141.1 5005 /step_next i 255

#OSC connection to QLC+
clientQLC = udp_client.SimpleUDPClient("10.3.141.1", 5005)

DELAY = 0.5

for currentSong in SName:

  currentMessage = "/start_cuelist/" + SName[currentSong]
  print (currentMessage)
  
    
  clientQLC.send_message(currentMessage, 255)
  clientQLC.send_message(currentMessage, 0)


  time.sleep(DELAY)

  print ("    Next step")
  clientQLC.send_message("/step_next", 255)
  clientQLC.send_message("/step_next", 0)

  time.sleep(DELAY)
  print ("    Previous step")
  clientQLC.send_message("/step_previous", 255)
  clientQLC.send_message("/step_previous", 0)

  time.sleep(DELAY)


  
  print ("    Stop")
  clientQLC.send_message("/stop", 255)
  clientQLC.send_message("/stop", 0)
  clientQLC.send_message("/stop", 255)
  clientQLC.send_message("/stop", 0)

  time.sleep(DELAY)


