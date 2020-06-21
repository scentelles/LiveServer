import sys  
sys.path.append("..")  

import json

#obs-websocket-py package
from obswebsocket import obsws, requests

#python-osc package
from pythonosc import osc_server
from pythonosc import dispatcher
from pythonosc import udp_client
import threading

#pywin32 package
import win32com.client
import time

from SmoothDefines import *

MAIN_LOOP_DELAY = 0.01 #TODO : replace loop with message queue

with open('config.json') as config_file:
    config = json.load(config_file)

OSC_LOCALHOST_IP   = config['OSC_LOCALHOST_IP']
OSC_LOCALHOST_PORT = config['OSC_LOCALHOST_PORT']
OSC_PROJECTM_PORT  = config['OSC_PROJECTM_PORT']

OBS_HOST = config['OBS_HOST']
OBS_PORT = config['OBS_PORT']
OBS_PWD  = config['OBS_PWD']

SLIDESHOW_PATH = config['SLIDESHOW_PATH']

ws = obsws(OBS_HOST, OBS_PORT, OBS_PWD)
obs_connected = False


clientProjectM = udp_client.SimpleUDPClient(OSC_LOCALHOST_IP, OSC_PROJECTM_PORT)



currentSong = 0

initialized = False

NO_COMMAND 		= 0
NEXT_SLIDE 		= 1
PREVIOUS_SLIDE 	= 2
START_SONG 		= 3
CHRIS_TALK 		= 4

localCommand = NO_COMMAND

ScenesNames = []

     

app = win32com.client.Dispatch("PowerPoint.Application")


class ppt:
	def __init__(self):
		
		self.pres = app.Presentations.Open(SLIDESHOW_PATH, WithWindow=False)
	
	def goto_slide(self, nb):
		try:
			print("Setting slide " + str(nb))
			self.pres.SlideShowWindow.View.GotoSlide(nb)
		except:
			print("Exception when trying to set slide. Please kill ALL ppt instances from task manager ")
	def next_slide(self):
		self.pres.SlideShowWindow.View.Next() 

	def previous_slide(self):
		self.pres.SlideShowWindow.View.Next() 
		
	def start_slideshow(self):

		#self.pres.SlideShowSettings.LoopUntilStopped = True
		#self.pres[index].SlideShowSettings.ShowMediaControls = False
		self.pres.SlideShowSettings.Run()
		#app.WindowState = 1

	def stop_slideshow(self):
		#self.pres[self.active_pres].SlideShowWindow.View.Exit()
		#app.WindowState = 2
		time.sleep(1)
		app.SlideShowWindows(1).View.Exit()
		self.active_pres = -1

def startSongSlide(song):
	global my_slide	
	slideNb = SToSlide[song]
	print("Setting ppt slide according to song : " + str(slideNb))
	my_slide.goto_slide(slideNb)
		
	
		
def song_osc_receive(unused_addr, args, songNb):
  print("\n[{0}] ~ {1} ".format(args[0], songNb))
  print("Requesting start song to ppt local command loop")
  global currentSong
  global localCommand
  currentSong = songNb
  localCommand = START_SONG  
  

   

def slideshow_osc_receive(unused_addr, args, command):
  global localCommand 
  if(command == SLIDESHOW_COMMAND_NEXT_SLIDE):
    localCommand = NEXT_SLIDE
  if(command == SLIDESHOW_COMMAND_PREVIOUS_SLIDE):
    localCommand = PREVIOUS_SLIDE	
	
    
  print("\n[{0}] ~ {1} ".format(args[0], command))
   

#TODO check works from RASPI/QLC changes   
def obs_osc_receive(unused_addr, args, command, value):
	global obs_connected
	if(obs_connected):
		if(command == OBS_COMMAND_SWITCH_SCENE):
			ws.call(requests.SetCurrentScene(ScenesNames[value])) 	
	else:
		print("Warning: OBS not connected. Skipping OBS OSC command")
	print("\n[{0}] ~ {1} {2}".format(args[0], command, value))
  
def projectm_preset_osc_receive(unused_addr, args, preset):
	#send preset
	clientProjectM.send_message("/projectm/preset", preset)
	print("\n[{0}] ~ {1}".format(args[0], preset))  
 
def projectm_command_osc_receive(unused_addr, args, command, value):
	#send command to projectM
	if(command == 1):
		clientProjectM.send_message("/projectm/lock", value);
	if(command == 2):
		clientProjectM.send_message("/projectm/random", value);

	print("\n[{0}] ~ {1} {1}".format(args[0], command, value))  
	
 
def osc_thread(name):
	dispatcher.map("/video/song", song_osc_receive, "song_osc_receive")
	dispatcher.map("/video/slideshow", slideshow_osc_receive, "slideshow_osc_receive")

	dispatcher.map("/video/obs", obs_osc_receive, "obs_osc_receive")
	dispatcher.map("/video/projectm/preset", projectm_preset_osc_receive, "projectm_preset_osc_receive")
	dispatcher.map("/video/projectm/command", projectm_command_osc_receive, "projectm_command_osc_receive")
	
	server = osc_server.ThreadingOSCUDPServer((OSC_LOCALHOST_IP, OSC_LOCALHOST_PORT), dispatcher)
	print("Starting OSC server")
	try:
		server.serve_forever()
	except (KeyboardInterrupt, SystemExit):
		print('The END in OSC server.')

	
		
my_slide = ppt()
time.sleep(1)
my_slide.start_slideshow()

time.sleep(2)

dispatcher = dispatcher.Dispatcher()
x = threading.Thread(target=osc_thread, args=(1,))

x.start()


def obs_connect():	
	global obs_connected
	try:
		print("Connecting to OBS\n")
		ws.connect()	
		obs_connected = True
	except:
		print("ERROR : could not connect to OBS. Is OBS running?\n")
		return
	scenes = ws.call(requests.GetSceneList())
	for s in scenes.getScenes():
		name = s['name']
#            print(ws.call(requests.GetSourcesList()),"\n")       # Get The list of available sources in each scene in OBS
		ScenesNames.append(name)                        # Add every scene to a list of scenes
	print("\n CURRENT SCENES IN OBS" ,ScenesNames)
	
	
try:
	while True:
		time.sleep(MAIN_LOOP_DELAY)
		if (localCommand != NO_COMMAND):
			if(obs_connected == False):
				obs_connect()
			
			print("Executing local command")
			if localCommand == NEXT_SLIDE:
				my_slide.next_slide()
			if localCommand == PREVIOUS_SLIDE:
				my_slide.previous_slide()
			if localCommand == START_SONG:
				startSongSlide(currentSong)

			localCommand = NO_COMMAND
			
except KeyboardInterrupt:
	app.Quit()
	print('The END.')
