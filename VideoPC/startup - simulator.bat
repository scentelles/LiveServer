::start projectM
::start Musicbeam

start "Simulator" python -u ..\Simulator\simulator.py
timeout /t 2
start "Video Manager" python -u videoManager.py config.json

pushd .

timeout /t 2
::Path for obs config files : %appdata%/obs-studio
::https://obsproject.com/wiki/Launch-Parameters
cd %cd%\visualizer
start projectM.exe
cd "C:\Program Files\obs-studio\bin\64bit" 
start obs64.exe --profile "Smooth" --collection "Smooth" --scene "Default" --allow-opengl --minimize-to-tray

popd