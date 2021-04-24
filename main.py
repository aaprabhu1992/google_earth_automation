import argparse
import json
import pywinauto


import helper
import timelapse
import tour

parser = argparse.ArgumentParser()
parser.add_argument('-param',
                    type=str,
                    help='Param JSON', required = False)
args = parser.parse_args()


paramJSON = {}
if args.param is not None:
    try:
        with open(args.param, "r") as f:
            paramJSON = json.load(f)
    except OSError:
        print("File Read Error")
    helper.PrettyPrintJSON(paramJSON)


# Import pywinauto Application class
from pywinauto.application import Application
# Start a new process and specify a path to the text file
app = Application().start('"C:/Program Files/Google/Google Earth Pro/client/googleearth.exe"', timeout=helper.WAIT_WINDOW)


helper.PauseForEffect(helper.MEDIUM_PAUSE)
dlg_spec = app.window()


# Resize the window
x, y = helper.LocateImage('./common/restore.png')
if x != None and y != None:
    helper.LocateAndClick('./common/restore.png', helper.SMALL_PAUSE)
helper.LocateAndClick('./common/maximize.png', helper.SMALL_PAUSE)


x, y = helper.LocateImage('./common/closeIntro.png')
if x != None and y != None:
    helper.LocateAndClick('./common/closeIntro.png', helper.SMALL_PAUSE)


if paramJSON:
    assert "data" in paramJSON, "Data parameter not provided"
    allData = paramJSON["data"]
    for data in allData:
        assert "type" in data, "Type Parameter not provided"
        if data["type"] == "TIMELAPSE":
            timelapse.record(data)
        elif data["type"] == "BNA":
            timelapse.record(data)
        elif data["type"] == "TOUR":
            tour.record(data)
        else:
            print("TYPE not recognized")
