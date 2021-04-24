# Tour needs the following things
# 1. The tour should have all the locations
# 2. Time Stamp should be there as that will be replaced in new KML
# 3. Start Point will be chosen by default
# 4. It will create a new local KML file with the Date
# 5. Google Earth should be open with places already expanded
# 6. Add the new KML
# 7. Start recording
# 8. Play tour for the temp folder
# 9. Record till atleast 10 times the image is repeated
# 10. Stop Tour
# 11. Clear Temp Folder Contents
import pyautogui
import math
import os
from PIL import ImageChops
import cv2
import numpy as np
import glob
import time

import helper
import videoCreator

# this will have to be determined based on the device
IMAGE_WIDTH = 2600
IMAGE_HEIGHT = 1420
imageRegion = (590, 170,IMAGE_WIDTH, IMAGE_HEIGHT) 
closeX = 50
closeY = -50


#CONSTANTS (Independent of the screen resolution)
DEFAULT_VIDEO_NAME = "video"
DEFAULT_VIDEO_CODEC = "MP4V"
DEFAULT_VIDEO_FPS = 3
SCROLL_AMOUNT = 30
DEFAULT_SCREENSHOT_NAME = "screenshot_tour_.jpg"

def EndReached(start, totalTime):
    end = time.time()
    if end - start < totalTime:
        return False
    else:
        return True
    # x, y = helper.LocateImage("./common/videoEnd.png")
    # if x != None and y != None:
        # return True
    # else:
        # return False


def CheckJSON(inputJSON):
    assert "file" in inputJSON, "Initial File has to be provided"
    assert "dates" in inputJSON, "At least 1 date has to be provided"
    

def GetNewFileName(inputFileName, inputDate):
    pathVal, fileName = os.path.split(inputFileName)
    fileName, extension = os.path.splitext(fileName)
    return os.path.join(pathVal, fileName + inputDate + extension)
    

def CreateNewKMLFile(inputFileName, inputDate):
    newFileName = GetNewFileName(inputFileName, inputDate)
    print("New File Name: {}".format(newFileName))
    lines = []
    with open(inputFileName, "r") as f:
        lines = f.readlines()
    newLines = []
    for line in lines:
        newLines.append(line)
    with open(newFileName, "w") as f:
        f.writelines(newLines)
    print("Created a new file")
    return newFileName

def OpenFile(fileName):
    pyautogui.hotkey("ctrl", "o")
    helper.PauseForEffect(helper.SMALL_PAUSE)
    pyautogui.write(fileName)
    pyautogui.press(["enter"])



# pyautogui.click(button='right')
# pyautogui.press(["right"])
# pyautogui.press(["down", "down", "down"])
def CreateTour(inputFileName, totalTime):
    # Video Details
    pathVal, fileName = os.path.split(inputFileName)
    fileName, extension = os.path.splitext(fileName)
    videoName = fileName + helper.videoExtensionMap[helper.VideoCodec[DEFAULT_VIDEO_CODEC]]
    fourcc = cv2.VideoWriter_fourcc(*DEFAULT_VIDEO_CODEC)
    out = cv2.VideoWriter(videoName, fourcc, DEFAULT_VIDEO_FPS, (IMAGE_WIDTH, IMAGE_HEIGHT))
    count = 0

    start = time.time()
    # Video Recording
    while not EndReached(start, totalTime):
        count += 1
        img = pyautogui.screenshot(DEFAULT_SCREENSHOT_NAME, region = imageRegion)
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
    print("Total Images Recorded: {}".format(str(count)))
    # Complete Recording
    x, y = pyautogui.position()
    helper.ClickAndWait(x + 2 * closeX, y, helper.SMALL_PAUSE)
    helper.LocateAndClick("./common/saveTour.png", helper.SMALL_PAUSE, adjX = closeX, adjY = closeY)
    helper.PauseForEffect(helper.SMALL_PAUSE)
    out.release()
   
def CleanUp():
    x, y = helper.LocateImage("./common/tempPlacesSelected.png")
    if x != None and y != None:
        helper.ClickAndWait(x, y, helper.SMALL_PAUSE)
        pyautogui.click(button = 'right')
        pyautogui.press(["down", "down", "down"])
        pyautogui.press(["enter"])
        helper.PauseForEffect(helper.SMALL_PAUSE)
        pyautogui.press(["enter"])

def RecordTour(fileName, totalTime):
    x, y = helper.LocateImage("./common/tempPlacesNotSelected.png")
    if x != None and y != None:
        helper.ClickAndWait(x, y, helper.SMALL_PAUSE)
    helper.LocateAndClick("./common/recordTour.png", helper.SMALL_PAUSE)
    CreateTour(fileName, totalTime)
    
def CreateAndRecord(inputFileName, inputDate, totalTime):
    fileName = CreateNewKMLFile(inputFileName, inputDate)
    print("Opening File")
    helper.PauseForEffect(helper.SMALL_PAUSE)
    print(os.path.join(os.getcwd(), "StartPoint.kml"))
    OpenFile(os.path.join(os.getcwd(), "StartPoint.kml"))
    helper.PauseForEffect(helper.SMALL_PAUSE)
    OpenFile(fileName)
    helper.PauseForEffect(helper.SMALL_PAUSE)
    RecordTour(fileName, totalTime)
    helper.PauseForEffect(helper.SMALL_PAUSE)
    CleanUp()





def record(inputJSON):
    CheckJSON(inputJSON)
    helper.PauseForEffect(helper.SMALL_PAUSE)
    allDates = inputJSON["dates"]
    for date in allDates:
        CreateAndRecord(inputJSON["file"], date, inputJSON["time"])
    
