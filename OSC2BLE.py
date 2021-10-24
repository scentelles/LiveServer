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

if(len(sys.argv) > 1):
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    videoPC_ip = local_ip
else:
    from bluepy import btle
    #local_ip = "10.3.141.1"
    videoPC_ip = "10.3.141.52"


ledThreads = {}
MAC_ADDRESS_CHRIS = "ff:ff:ee:00:27:09"
MAC_ADDRESS_SLY   = "ff:ff:10:0f:53:11"
MAC_ADDRESS_GUI   = "ff:ff:bc:00:2b:78"
MAC_ADDRESS_LED4  = "ff:ff:ac:00:24:1b"
MAC_ADDRESS_TEST  = "ff:ff:10:0f:51:dc"

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

  #Channels >= 15 => OSC controls of Megascreen, VideoPC, etc...
  if(int(channel) >= 15):
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
 

  
  #print("address" + osc_address + " : " + str(ledIndex) + " : " + str(channelIndex) + " : " + str(value))
  
  #For channes < 15, BLE controls
  else: #for DMX channel between 0 and 15)
    myLed = ledThreads[ledIndex]

    if (myLed.connected):
             #   print(str(myLed.name) + " : " + str(value))
                if(channelIndex == 0):
                   myLed.R = value
                if(channelIndex == 1):
                   myLed.G = value
                if(channelIndex == 2):
                   myLed.B = value

                #TODO: FIX. workaround because too many messages, losing some values.
               # if(myLed.R + myLed.R + myLed.R <60) :
                #    myLed.R = 0
                 #   myLed.G = 0
                  #  myLed.B = 0
                try:	               
                  myLed.bleWrite()
                  #time.sleep(0.2) #change debug
                except Exception as e:
                  print('Exception : Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                  print("DISCONNECTED!!!!!!!")
                  myLed.connected = 0
                  myLed.connect()

    else:
      print("Received command, but still not connected to " + str(myLed.name) + ". Trying to connect now")
      myLed.connect()



class MonThread (threading.Thread):
    def __init__(self, macAddress, name):     
        threading.Thread.__init__(self) 
        print(macAddress)
        self.macAddress = macAddress
        self.connected = 0
        self.char = 0
        self.dev = 0
        self.service = 0
        self.R = 0
        self.G = 0
        self.B = 0
        self.name = name
        self.connectionOngoing = 0
        self.lastBleWriteTime = 0
        self.lastValuesSent = 1
	
    def hello():
        print("Hello")
	
    def bleWrite(self):
        
        if(time.time() - self.lastBleWriteTime > DEBOUNCE_DELAY):
            print("R :" + str(self.R) + "G : " + str(self.G) + "B : " + str(self.B))
            self.char.write(bytes([0x56,  self.R, self.G, self.B, 0x00, 0xf0, 0xaa]))
            self.lastBleWriteTime = time.time()
        else:
            print("debouncing BLE write")
            self.lastValuesSent = 0    

    def connect(self):
                if(self.connectionOngoing == 0):
                    self.connectionOngoing = 1
                    print("trying to connect to " + self.name)
                    try:
                        self.dev = btle.Peripheral(self.macAddress)
                        self.service = self.dev.getServiceByUUID("0000FFE5-0000-1000-8000-00805F9B34FB")
                        self.char = self.service.getCharacteristics("0000FFE9-0000-1000-8000-00805F9B34FB")[0]  
                        self.connected = 1
                        print("Connected successfully to " + self.name)
                        self.connectionOngoing = 0
                    except:
                        print ("connection failed")
                        self.connected = 0  
                        self.connectionOngoing = 0			
	    
                else:
                    print("           Connection already on going")
    
    def run(self):
 
        if (self.connected == 0):
            self.connect()
        while 1:
            if (self.connected):

                #print (time.time())
                if((time.time() - self.lastBleWriteTime > DELAY_TO_SEND_LAST_VALUES) and (self.lastValuesSent == 0)): #Send last values afer delay without ble write
                    print("Sending last values")
                    try:	
                        self.bleWrite()
                        self.lastValuesSent = 1
                    except Exception as e:
                        print("DISCONNECTED!!!!!!!")
                        print('Exception : Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                        #self.connected = 0
                        #self.connect()


            time.sleep(0.1)



dispatcher = dispatcher.Dispatcher()
dispatcher.map("/*", dispatch_qlc_osc_handler, "QLC")

server = osc_server.ThreadingOSCUDPServer((OSC_ADDRESS, OSC_PORT), dispatcher)
print("Serving on {}".format(server.server_address))

m = MonThread(MAC_ADDRESS_CHRIS, "LedChris") 
m2 = MonThread(MAC_ADDRESS_SLY, "LedSly")          
m3 = MonThread(MAC_ADDRESS_GUI, "LedGui")          
m4 = MonThread(MAC_ADDRESS_LED4, "Led4")          
m5 = MonThread(MAC_ADDRESS_TEST, "LedTest")   

ledThreads[0] = m
ledThreads[1] = m2
ledThreads[2] = m3
ledThreads[3] = m4
ledThreads[4] = m5

m.start()                  
m2.start() 
m3.start() 
m4.start() 
m5.start() 



server.serve_forever()


     


