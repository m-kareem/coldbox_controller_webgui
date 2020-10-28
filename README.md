# coldbox_controller_WebGUI


example of a running server:
http://petra.phys.yorku.ca:5000



Installation
------------
1. Copy/clone the source code to the server computer
2. Install Python 3 and pip3 (if they are not already installed)
3. a) In development: Install the dependencies required for the gui to run:
    `pipenv install --dev`

   b) In production:
    `pipenv install --ignore-pipfile`


- to run the web-gui, execute `python3 coldbox_controller_webgui.py -c configFile.conf [-v]`


To do next
----------
- implement python logging
- implement user login feature with user management
