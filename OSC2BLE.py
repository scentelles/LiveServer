#!/usr/bin/env python3
from bluepy import btle
import time
import threading
import sys
from threading import Timer


from pythonosc import osc_server
from pythonosc import dispatcher


ledThreads = {}
MAC_ADDRESS_CHRIS = "ff:ff:ee:00:27:09"
MAC_ADDRESS_SLY   = "ff:ff:10:0f:53:11"
MAC_ADDRESS_GUI   = "ff:ff:bc:00:2b:78"
MAC_ADDRESS_LED4  = "ff:ff:ac:00:24:1b"
MAC_ADDRESS_TEST  = "ff:ff:10:0f:51:dc"

OSC_ADDRESS   = "127.0.0.1"
OSC_PORT      = 9002         #corresponds to universe #3

DEBOUNCE_DELAY = 0.2
DELAY_TO_SEND_LAST_VALUES = 1




def dispatch_qlc_osc_handler(osc_address, args, command):

  global ledThreads


  channel = (osc_address.split("/"))[3]
  ledIndex = int(int(channel)/3)
  channelIndex = int(channel)%3
  value = round(command*255)
  
  
  #print("address" + osc_address + " : " + str(ledIndex) + " : " + str(channelIndex) + " : " + str(value))
  
  
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
                if(myLed.R + myLed.R + myLed.R <60) :
                    myLed.R = 0
                    myLed.G = 0
                    myLed.B = 0
                #myLed.dev.connect() 	
                try:	               
                  myLed.bleWrite()
                  # time.sleep(0.2)
                except:
                  print("Lost connection")
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

    def hello():
        print("Hello")
	
    def bleWrite(self):
        
        if(time.time() - self.lastBleWriteTime > DEBOUNCE_DELAY):
            self.char.write(bytes([0x56,  self.R, self.G, self.B, 0x00, 0xf0, 0xaa]))
            self.lastBleWriteTime = time.time()
        else:
            print("debouncing BLE write")

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

        if (self.connected):
            while 1:
                if(time.time() - self.lastBleWriteTime > DELAY_TO_SEND_LAST_VALUES): #Send last values afer delay without ble write
                    #print("Sending last values")
                    self.bleWrite()
                   # self.lastValuesSent = 1
                time.sleep(1)



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


     


