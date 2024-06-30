import time
import logging

import rtmidi
from rtmidi.midiutil import open_midiinput

INPUT_PORT  = 'Springbeats vMIDI8'
OUTPUT_PORT = 'Springbeats vMIDI4'


  
class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()
        self.scheduled_timer = None
        self.toggle = [0 for x in range(128)]

    def toggleCC(self, ccId):

      if(self.toggle[ccId] == 0):
        print("toggling ON")
        cc = [0xB0, ccId, 127]    # CC - ON
        if((ccId >3) and (ccId < 8)):
            for i in range(8): 
                self.toggle[i] = 0
        
        self.toggle[ccId] = 1
        

        
        
      else:
        print("toggling OFF")
        cc = [0xB0, ccId, 0]      # CC - OFF
        self.toggle[ccId] = 0
      midiout.send_message(cc) 
              
    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        #Forward program changes received from Voicelive
        if(message[0] == 0xB0):
           #receive CC

           ccId = message[1]
           print("CC " + str(ccId) + " received")
           self.toggleCC(ccId)
        

#Open output port
midiout = rtmidi.MidiOut()
ports = midiout.get_ports()
for port, name in enumerate(ports):
    print("[%i] #%s#" % (port, name))
    if(OUTPUT_PORT in name):
       print("Opening output port [%i] #%s#" % (port, name))
       midiout.open_port(port)

log = logging.getLogger('midiin_callback')
logging.basicConfig(level=logging.DEBUG)

#Open input port
midiin = rtmidi.MidiIn()
ports = midiin.get_ports()
for port, name in enumerate(ports):
    print("[%i] #%s#" % (port, name))
    if(INPUT_PORT in name):
       print("Opening input port [%i] #%s#" % (port, name))
       midiin.open_port(port)
       port_name = name
       
       
midiin.set_callback(MidiInputHandler(port_name))

while(1):
    try:
        print("Entering main loop. Press Control-C to exit.")
        time.sleep(1)
        
    except KeyboardInterrupt:

        exit()
