import json
import time
import pyautogui
from enum import Enum

MIN_SLEEP_TIME = 10


SMALL_PAUSE = 3
MEDIUM_PAUSE = 10
LARGE_PAUSE = 20    
WAIT_WINDOW = 40

class ImageType (Enum):
    JPEG = 1
    PNG = 2
    BMP = 3

imageTypeMap = {}
imageTypeMap[ImageType['JPEG']] = ".jpg"
imageTypeMap[ImageType['PNG']] = ".png"
imageTypeMap[ImageType['BMP']] = ".bmp"


class VideoCodec (Enum):
    MP4V = 1
    XVID = 2

    
videoExtensionMap = {}
videoExtensionMap[VideoCodec['MP4V']] = ".mp4"
videoExtensionMap[VideoCodec['XVID']] = ".avi"


def PrettyPrintJSON(jsonObj, jsonIndent = 3):
    print(json.dumps(jsonObj, indent = jsonIndent))


def PauseForEffect(inputTime):
    while inputTime > 10:
        time.sleep(MIN_SLEEP_TIME)
        inputTime -= 10
        print("Waited for 10 sec, Time Left: {}".format(inputTime))
    time.sleep(inputTime)




def LocateImage(templateImageLocation, confidence_input = 0.9):
    x = None
    y = None
    try:
        x, y = pyautogui.locateCenterOnScreen(templateImageLocation, grayscale = True, confidence= confidence_input)
        print("Button FOUND : {}".format(templateImageLocation))
    except:
        print("Button not Found : {}".format(templateImageLocation))
    return x, y
def ClickAndWait(x,y, waitTime = 0):
    if x != None and y != None:
        pyautogui.click(x,y)
        if waitTime > 0:
            PauseForEffect(waitTime)
    else:
        exit(1)

def LocateAndClick(templateImageLocation, waitTime = 0, adjX = 0, adjY = 0, confidence_input = 0.9):
    x, y = LocateImage(templateImageLocation, confidence_input)
    ClickAndWait(x + adjX, y + adjY, waitTime)
