::start projectM
::start Musicbeam

start py videoManager.py
pushd .

sleep 2
::Path for obs config files : %appdata%/obs-studio
::https://obsproject.com/wiki/Launch-Parameters
cd "C:\Program Files\obs-studio\bin\64bit" 
start obs64.exe --profile "Smooth" --collection "Smooth" --scene "Default" --allow-opengl --minimize-to-tray
cd C:\Users\az02098.CORP\source\repos\projectm\msvc\projectM-sdl\Release
start projectM.exe
popd