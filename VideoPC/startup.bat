::start projectM
::start Musicbeam

start "Video Manager" python -u videoManager.py config.json
pushd .

timeout /t 2
::Path for obs config files : %appdata%/obs-studio
::https://obsproject.com/wiki/Launch-Parameters
cd "C:\Program Files\obs-studio\bin\64bit" 
start obs64.exe --profile "Smooth" --collection "Smooth" --scene "Default" --allow-opengl --minimize-to-tray
popd
cd visualizer
start projectM.exe
cd ..