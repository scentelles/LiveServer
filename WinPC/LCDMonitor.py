import usb1

from lcd2usb import LCD
import random
import time
import statistics

import psutil

import threading



class LCDMonitorThread (threading.Thread):
    def __init__(self, myLcd):      
        threading.Thread.__init__(self) 
        self.myLcd = myLcd          
        self.memoryValues = [0,0,0,0]
		
    def run(self):
      lcd = self.myLcd
      memoryValues = self.memoryValues
      while(1):
        msg = 'CPU : ' +  str(psutil.cpu_percent(interval=1))
        lcd.clear()
        lcd.goto(0, 0)
        lcd.write(msg)

        memoryStat = dict(psutil.virtual_memory()._asdict())
        memTotal = memoryStat["total"]
        memUsed = memoryStat["used"]
        memPercent = round((float(memUsed)/memTotal)*100, 1)
	  
        #print(self.getUpdatedVariance(memoryValues, memPercent))
      
        msg = 'Mem : ' +  str(memPercent)
        lcd.goto(0, 1)
        lcd.write(msg)
        
    def getUpdatedVariance(self, valueList, newValue):
        valueList.insert(0, newValue)
        valueList.pop()
        #print (valueList)
        #print(statistics.variance(valueList))       
	
    def join(self):
      self.die = True
      super().join()
			
							   


class LCDKeysThread (threading.Thread):
    def __init__(self, myLcd):      
        threading.Thread.__init__(self) 
        self.myLcd = myLcd          
    
    #todo : register callback to trigger custom actions
    def run(self):
        while(1):
            key1, key2 = self.myLcd.keys
            if(key1):
                keyVal = 1
            else:
                keyVal = 0
        
            #self.myLcd.goto(14, 0)
            #self.myLcd.write(str(keyVal))
	  
            if(key2):
                keyVal = 1
            else:
                keyVal = 0
            
            #self.myLcd.goto(14, 1)
            #self.myLcd.write(str(keyVal))
	  
            time.sleep(0.2)
            
class LCDMonitorClass:
    def __init__(self):      
        #list_usb()
        self.myLcd = LCD.find_or_die()

        # adjust contrast and brightess
        self.myLcd.set_contrast(200)
        self.myLcd.set_brightness(255)

        self.myLcd.clear()
        msg = "Starting ..."
        self.myLcd.write(msg)
        time.sleep(1)
        self.myLcd.clear()
        
        processesReady = False
        while(processesReady == False):
            process1Ready = self.checkProcessExists("TransMIDIfier.exe")
            if(process1Ready):
                msg = "TransMIDIfier OK"
                self.myLcd.clear()
                self.myLcd.write(msg)
                time.sleep(2)                

            process2Ready = self.checkProcessExists("Omnisphere.exe")
            if(process2Ready):
                msg = "Omnisphere OK"
                self.myLcd.clear()
                self.myLcd.write(msg)
                time.sleep(2)                
               
            processesReady = process1Ready and process2Ready
            time.sleep(1)
        
        msg = "Ready to Go!"
        self.myLcd.clear()
        self.myLcd.write(msg)
        time.sleep(1)
        
        self.monitorThread = LCDMonitorThread(self.myLcd)         
        self.monitorThread.start()                  

        self.keyThread = LCDKeysThread(self.myLcd)         
        self.keyThread.start()
        #self.lcdLoop()

    def checkProcessExists(self, myProcess):
        #for p in psutil.process_iter():
        #  print(p.name())
        #die()
        if(myProcess in (p.name() for p in psutil.process_iter())):
            print(myProcess + " program found to be running")
            return True
        else:
            print("ERROR : " + myProcess + " not found in running processes")
            return False
 
    def lcdLoop(self):
        try:
            while(1):  
                time.sleep(1)
	  
        except KeyboardInterrupt:
            self.monitorThread.join()
            self.keyThread.join()


