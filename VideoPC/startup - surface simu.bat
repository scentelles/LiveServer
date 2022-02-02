::start projectM
::start Musicbeam

::start "transmidifier" /min "C:\Program Files (x86)\TransMIDIfier\TransMIDIfier.exe"
::timeout /t 1




start "Cantabile" "C:\Program Files\Topten Software\Cantabile 3.0\Cantabile.exe"
start /min "Midi2OSC" python -u ..\WinPC\Midi2OSC.py
timeout /t 1
start /min "OSC_QLC_DISPATCH" python -u ..\OSC_qlc_out_dispatcher.py
::timeout /t 1
::start "Kontakt" "C:\Program Files\Native Instruments\Kontakt\Kontakt.exe"
::timeout /t 1

start C:\QLC+\qlcplus.exe -p -o ..\QLC_setup.qxw
timeout /t 1

start /min "VoiceLiveSimu" python -u ..\Simulator\voicelive_simulator.py simulation_mode
::timeout /t 1
start /min "VideoManager" python -u videoManager.py config.json
timeout /t 2
start /min "LiveServer" python -u ..\LiveServerWindows.py 
::timeout /t 2
start /min "KeypressManager" python -u ..\keypressManager.py 
::timeout /t 2
pushd .

timeout /t 2
::Path for obs config files : %appdata%/obs-studio
::https://obsproject.com/wiki/Launch-Parameters
cd %cd%\visualizer
start "projectM" /min projectM.exe
cd "C:\Program Files\obs-studio\bin\64bit" 
start "OBS" obs64.exe --profile "Smooth" --collection "Smooth" --scene "Default" --allow-opengl --minimize-to-tray

popd