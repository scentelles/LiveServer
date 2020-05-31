import sys  
sys.path.append("..")  

#python-osc package
from pythonosc import osc_server
from pythonosc import dispatcher
import threading

#pywin32 package
import win32com.client
import pythoncom
import time

from SmoothDefines import *

MIDI_CONTROL_CHANGE = 0xb0
MIDI_PROGRAM_CHANGE = 0xc0
MIDI_CONTROL_CHANGE_FROM_CHRIS = 0x20 #Warning : this value is also received from voicelive...


LOCALHOST_IP   = "192.168.1.51"
LOCALHOST_PORT = 5007


currentSong = 0
chrisTalkOngoing = 0

initialized = False

NO_COMMAND 		= 0
NEXT_SLIDE 		= 1
PREVIOUS_SLIDE 	= 2
START_SONG 		= 3
CHRIS_TALK 		= 4

localCommand = NO_COMMAND

app = win32com.client.Dispatch("PowerPoint.Application")
# Create id
ppt_id = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, app)

class ppt:
	def __init__(self):

		self.pres = app.Presentations.Open(r'C:\Users\scent\Documents\LiveServer\VideoPC\clip1.ppsx',    WithWindow=False)
	
	def goto_slide(self, nb):
		self.pres.SlideShowWindow.View.GotoSlide(nb)
		
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
	my_slide.goto_slide(SToSlide[song])
		
def SmoothTrioPC():
  global currentStep
  global currentSong
  global localCommand
  
  if((currentSong in SName) and (chrisTalkOngoing == 0)): 
    print("setting local command start song")
    localCommand = START_SONG  

  else:
    print("Smooth song unmapped. do nothing")

#TODO: remove voicelive duplication beween receivers, need voicelive / smooth class    
def SmoothTrioCC(myCC, value):
	global chrisTalkOngoing
	global currentSong
	global localCommand
  
	#checking only CC coming from Chris
	if (myCC == MIDI_CONTROL_CHANGE_FROM_CHRIS) : 
		if(value == 125):
			print("From Chris : next video step")
			localCommand = NEXT_SLIDE
		elif(value == 124):
			print("From Chris : previous video step")
			localCommand = PREVIOUS_SLIDE     
		elif(value == 1):
			print("Setting Chris Talk Video Scene")

			if(chrisTalkOngoing == 0):
				chrisTalkOngoing = 1
				localCommand = CHRIS_TALK 

			else:  #restart show of current song when going out of CHris talk
				print("Exiting Chris Talk, starting song slide")
				chrisTalkOngoing = 0
				localCommand = START_SONG    

	else:
		print("Message from Chris unrecognized : " + str(value))
		
		
def forwardPCFromVoicelive(myCC, value):
  global currentSong
  songName = ""
  currentSong = myCC + 1
  if(currentSong in SName):
    songName = SName[currentSong]
  print("Setting current song to : " + str(currentSong) + " (" + songName + ")")
    
  if(currentSong > SMOOTH_PRESET_MIN and currentSong < SMOOTH_PRESET_MAX):
    SmoothTrioPC()

  else:
    #TODO : manage out of smooth presets cases
    print("Other songs than smooth ones to be managed")
		
def forwardCCFromVoicelive(myCC, value):
  global clientQLC
  print("Dispatching message CC from Voicelive : CC : " + str(myCC) + " | " + str(value))
  if(currentSong > SMOOTH_PRESET_MIN and currentSong < SMOOTH_PRESET_MAX):
    SmoothTrioCC(myCC, value)
  
		
def voicelive_osc_receive(unused_addr, args, command, note, vel):
  global initialized
  if(initialized == False):
    pythoncom.CoInitialize()
    appT = win32com.client.Dispatch(pythoncom.CoGetInterfaceAndReleaseStream(ppt_id, pythoncom.IID_IDispatch))
    initialized = True
  
  if(command == MIDI_CONTROL_CHANGE):
    forwardCCFromVoicelive(note, vel)

  if(command == MIDI_PROGRAM_CHANGE):
    print("MIDI_PROGRAM_CHANGE")
    forwardPCFromVoicelive(note, vel)

    
  print("\n[{0}] ~ {1} {2} {3}".format(args[0], command, note, vel))
   

def osc_thread(name):

	dispatcher.map("/midi/voicelive", voicelive_osc_receive, "voicelive_osc_receive")

	server = osc_server.ThreadingOSCUDPServer((LOCALHOST_IP, LOCALHOST_PORT), dispatcher)
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
	
try:
	while True:
		time.sleep(0.01)
		if (localCommand != NO_COMMAND):
			print("Executing local command")
			if localCommand == NEXT_SLIDE:
				my_slide.next_slide()
			if localCommand == PREVIOUS_SLIDE:
				my_slide.previous_slide()
			if localCommand == START_SONG:
				startSongSlide(currentSong)
			if localCommand == CHRIS_TALK:
				my_slide.goto_slide(CHRIS_TALK_SLIDE_INDEX)
			localCommand = NO_COMMAND
			
except KeyboardInterrupt:
	app.Quit()
	print('The END.')
