from lcd2usb import LCD
import time
import os

import psutil

import RPi.GPIO as GPIO

import threading

import netifaces as ni

ttyActive = False
cnxSkip = False

lcd = LCD()

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;


def ttyMonitor(name):
	ttyCount = 0
	ttyCurrent = 1
	ttyRecentActivity = False
	global ttyActive
	while 1:
		ttyNew = GPIO.input(26)
		if(ttyNew != ttyCurrent):
			ttyRecentActivity = True
			ttyCurrent = ttyNew
			ttyActive = True 
			
		ttyCount += 1
		if(ttyCount > 50) : #After 5 seconds
			if(ttyRecentActivity == False):
				ttyActive = False
				
			ttyRecentActivity = False
			ttyCount = 0
			

		time.sleep(0.01)



GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("launching TTY monitor thread")
x = threading.Thread(target=ttyMonitor, args=(1,))
x.start()





lcd.info()



lcd.clear()
lcd.write('Connecting', 0, 0)
time.sleep(1)
count = 0
ip_address = ""
while 1:
	try:
		ip_address = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
	except KeyError :
		print("netif not yet available\n")
	print ("IP address : ", ip_address)
	if(ip_address == "10.3.141.2"):
		lcd.clear()
		lcd.write('Connected !', 0, 0)
		time.sleep(2)
		break
		
	elif(lcd.keys[0]):
		lcd.clear()
		lcd.write('Skipping cnx', 0, 0)
		cnxSkip = True
		time.sleep(2)
		break
	
	time.sleep(1)


lcd.clear()
lcd.write('QLC check', 0, 0)
time.sleep(1)
count = 0

while (checkIfProcessRunning("qlcplus") == False):
	time.sleep(0.2)
	if (count%15 == 0):
		lcd.write('               ', 0, 1)

	lcd.write('.', count%15, 1)
	count += 1

#if (cnxSkip == False):
#	lcd.clear()
#	lcd.write('LiveServer check', 0, 0)
#	time.sleep(1)
#	count = 0
#	while (checkIfProcessRunning("LiveServer") == False):
#		time.sleep(0.2)
#		lcd.write('.', count%15, 1)
#		count += 1
#	lcd.clear()
#	lcd.write('LiveServer OK', 0, 0)

	
lcd.clear()
lcd.write('Status : OK', 0, 0)
lcd.write('DMX : ', 0, 1)

dmxCount = 0




	
while 1:
	if(lcd.keys[0]):
		print("Shutting down !!!")
		lcd.clear()
		lcd.write('SHUTTING DOWN !!!', 0, 0)

		time.sleep(1)
		lcd.write('3', 0, 1)
		time.sleep(1)
		lcd.write('2', 0, 1)
		time.sleep(1)
		lcd.write('1', 0, 1)
				
		os.system("shutdown -P now")
	elif(lcd.keys[1]):
		print("switching QLC")
		os.system("pkill qlcplus")
		os.system("sudo -u pi /usr/bin/qlcplus -o /home/pi/Projects/LiveServer/QLC_setup-vindhelfest.qxw -p &")

	elif (ttyActive == True):
		print("DMX active")
		if (dmxCount%7 == 0):
			lcd.write('       ', 7, 1)	
		lcd.write('.', 7 + dmxCount%7, 1)
		dmxCount += 1
		if(dmxCount == 7):
			dmxCount = 0
	else:
		print("DMX OFF")
		
		lcd.write('OFF     ', 7 , 1)
		dmxCount = 0
	
	time.sleep(0.5)
	

