::start projectM
::start Musicbeam

::start "Simulator" python -u ..\Simulator\simulator.py
start "VoiceLiveSimu" python -u ..\Simulator\voicelive_simulator.py simulation_mode
timeout /t 1
start /min "Video Manager" python -u videoManager.py config.json
timeout /t 2
start /min "LiveServer" python -u ..\LiveServer.py simulation_mode
timeout /t 2
start /min "OSC2VIDEO" python -u ..\OSC2BLE.py simulation_mode

pushd .

timeout /t 2
::Path for obs config files : %appdata%/obs-studio
::https://obsproject.com/wiki/Launch-Parameters
cd %cd%\visualizer
start /min projectM.exe
cd "C:\Program Files\obs-studio\bin\64bit" 
start obs64.exe --profile "Smooth" --collection "Smooth" --scene "Default" --allow-opengl --minimize-to-tray

popd