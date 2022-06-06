/usr/bin/lxterm -title "LCD" -hold -e 'sudo /usr/bin/python3 /home/pi/Projects/LiveServer/LCD.py' &

/usr/bin/lxterm -title "QLC" -hold -e  '/usr/bin/qlcplus -o /home/pi/Projects/LiveServer/QLC_setup-raspi.qxw -p' &

sleep 20
echo "Launching LiveServer"

/usr/bin/lxterm -title "LiveServer" -hold -e '/usr/bin/python3 /home/pi/Projects/LiveServer/LiveServer.py' &

#echo "Launching OSC 2 BLE bridge"
#/usr/bin/lxterm -title "OSC2BLE" -hold -e '/usr/bin/python3 /home/pi/Projects/LiveServer/OSC2BLE.py'&

