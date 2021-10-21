Install obs studio : https://obsproject.com/fr/download
Install obswebsocket : https://github.com/Palakis/obs-websocket/releases/

In windows terminal launch : >obs-restore.bat

Launch OBS studio 
When prompted to configure websocket password, accept, 
and enter password : "secret"
Leave port to : "4444"


Install python (tested successfully with python 3.9 installed from microsoft store)
pip install obs-websocket-py
pip install pywin32

Update config.json SLIDESHOW_PATH variable with the path to the slideshow

For simulator : 
pip install prompt_toolkit
