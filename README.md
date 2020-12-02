# coldbox_controller_WebGUI


example of a running server:
http://petra.phys.yorku.ca:5000



Installation
------------
1. Copy/clone the coldjiglib2 libraries for: https://gitlab.cern.ch/ColdJigDCS/coldjiglib2.git in a
2. cd ../
3. Copy/clone the source code to the server computer
4. Install Python 3 and pip3 (if they are not already installed)
5. a) In development: Install the dependencies required for the gui to run:
    `pipenv install --dev`

   b) In production:
    `pipenv install --ignore-pipfile`

6. source setenv.sh

- to run the web-gui, execute `python3 coldbox_controller_webgui.py -c configFile.conf [-v]`
