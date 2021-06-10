#!/usr/bin/env python3

# Test file to test pypubsub
# this file is a fake coldjiglib that will be sending messages
#
# the defined messages topics are:
# - 'warning' : eg: "humidity increasing", "N2 flow low"
# - 'error' : eg: "No response from chiller", "can't connect to INFLUX"
# - 'alert' : "Turn down N2 flow", "Safe to open lid", "module QC completed"
# - 'danger' : "condensation on module", "interlock fired","Peltier overheating"
#

from pubsub import pub
import time

def start() :
    print("Starting fake coldjiglib")
    print("this fake coldjiglib is just sending out messages. Does not know who will receive them")
    print("wait 10s then send message")

    time.sleep(10)
    pub.sendMessage('alert',message="fake coldjiglib started")

    time.sleep(10)
    print("send warning")
    pub.sendMessage('warning',message="ohh....it's getting warm in here....")

    time.sleep(10)
    print("send error")
    pub.sendMessage('error',message="oh no - you sent me the wrong directions home")

    time.sleep(10)
    print("send danger")
    pub.sendMessage('danger',message="Klingons on the starboard bow!!")

    time.sleep(10)
    pub.sendMessage('alert',message='finished..')
