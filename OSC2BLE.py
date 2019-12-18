from bluepy import btle
import time
import threading
import sys


from pythonosc import osc_server
from pythonosc import dispatcher


ledThreads = {}
MAC_ADDRESS_CHRIS = "ff:ff:ee:00:27:09"
MAC_ADDRESS_SLY = "ff:ff:10:0f:53:11"
MAC_ADDRESS_GUI = "ff:ff:bc:00:2b:78"
MAC_ADDRESS_LED4 = "ff:ff:ac:00:24:1b"
MAC_ADDRESS_TEST = "ff:ff:10:0f:51:dc"

OSC_ADDRESS   = "127.0.0.1"
OSC_PORT      = 9002         #corresponds to universe #3

def dispatch_qlc_osc_handler(osc_address, args, command):

  global ledThreads


  channel = (osc_address.split("/"))[3]
  ledIndex = int(int(channel)/3)
  channelIndex = int(channel)%3
  value = round(command*255)
  
  
  print("address" + osc_address + " : " + str(ledIndex) + " : " + str(channelIndex) + " : " + str(value))
  
  
  myLed = ledThreads[ledIndex]

  if (myLed.connected):
                print(str(myLed.name) + " : " + str(value))
                if(channelIndex == 0):
                   myLed.R = value
                if(channelIndex == 1):
                   myLed.G = value
                if(channelIndex == 2):
                   myLed.B = value
		   
                #myLed.dev.connect() 	
                try:	               
                  myLed.char.write(bytes([0x56, myLed.R, myLed.G, myLed.B, 0x00, 0xf0, 0xaa]))
                  # time.sleep(0.2)
                except:
                  print("Lost connection")
                  myLed.connected = 0
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
	

    def connect(self):
                print("trying to connect to " + self.name)
                self.dev = btle.Peripheral(self.macAddress)
                self.service = self.dev.getServiceByUUID("0000FFE5-0000-1000-8000-00805F9B34FB")
                self.char = self.service.getCharacteristics("0000FFE9-0000-1000-8000-00805F9B34FB")[0]  
                self.connected = 1
                print("Connected successfully to " + self.name)

    
    def run(self):
 
        if (self.connected == 0):
            try:
                self.connect()
            except :
                print("Could not connect")	 
                self.connected = 0  
          
 
        i=0
        if (self.connected):
            while 1:
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


     


