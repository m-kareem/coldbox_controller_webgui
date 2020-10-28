
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

help = """
    -- ColdBox controller webGUI --
    Copyright (C) 2019-2020 CERN for the benefit of the ATLAS collaboration
    Author: mohammad.kareem@cern.ch

    Usage: coldbox_controller_webgui.py [arguments]

    Arguments:
    -c or --config <with file name>     Read GUI configurations from file.
    -v or --verbose                     Verbose printing

    -h or --help                        Print Help (this message) and exit
    """
    #-p or --port                        Port number (default port: 5000)

def CBC_help():
    print(bcolors.BOLD+ help+ bcolors.ENDC)
