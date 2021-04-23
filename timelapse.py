import pyautogui
import math
import os

import helper
import videoCreator


# this will have to be determined based on the device
backwardDelta = [-450, 150]
forwardDelta = [220, 150]
imageRegion = (590, 170,2600, 1420) 
searchBoxLocation = -200
centerOfPoint = 700
TIMELAPSE_IMAGE_NAME = "timelapse_"
DEFAULT_VIDEO_NAME = "video"
DEFAULT_VIDEO_CODEC = "MP4V"
DEFAULT_VIDEO_FPS = 3
SCROLL_AMOUNT = 30
# There has to be only one result available for this to work
def GoToPlace(inputPlace):
    helper.LocateAndClick('./common/search.png', adjX = searchBoxLocation)
    pyautogui.write(inputPlace, interval = 0.1)
    helper.LocateAndClick('./common/searchActive.png', helper.LARGE_PAUSE)
    helper.LocateAndClick('./common/closeSearch.png', helper.SMALL_PAUSE)
    

def GetMode(startVal, endVal):
    return (-1, 1)[startVal > endVal]
def record(inputJSON):
    helper.PauseForEffect(helper.SMALL_PAUSE)
    if "place" in inputJSON:
        GoToPlace(inputJSON["place"])
    if "scroll" in inputJSON:
        helper.LocateAndClick('./common/earth.png', helper.MEDIUM_PAUSE, adjY = centerOfPoint)
        for i in range(0,inputJSON["scroll"]):
            pyautogui.scroll(SCROLL_AMOUNT)

    assert "start_count" in inputJSON, "Need to Specify start count"
    assert "end_count" in inputJSON, "Need to Specify end count"
    assert "image_type" in inputJSON, "Need to Specify Image type for snapshot"
    
    # Locate Time Lapse
    x, y = helper.LocateImage('./common/timelapse.png')
    if x != None and y != None:
        # Start Time Lapse
        helper.ClickAndWait(x, y, helper.SMALL_PAUSE)
        startVal = inputJSON["start_count"]
        endVal = inputJSON["end_count"]
        assert startVal != endVal, "Start and End Cannot be the same"
        for i in range(0, startVal + GetMode(startVal, endVal)): # Need Extra as we are taking a snapshot after click
            helper.ClickAndWait(x + backwardDelta[0], y + backwardDelta[1])
                
        helper.PauseForEffect(helper.MEDIUM_PAUSE)
        print("Current Mode is {}".format(str(GetMode(startVal, endVal))))

        # Preprocessing before taking snapshot
        stepX = x
        stepY = y
        if GetMode(startVal, endVal) == -1:
            stepX = x + backwardDelta[0]
            stepY = y + backwardDelta[1]
        if GetMode(startVal, endVal) == 1:
            stepX = x + forwardDelta[0]
            stepY = y + forwardDelta[1]

        listToCapture = []
        # Capture All Steps
        if inputJSON["type"] == "TIMELAPSE":
            listToCapture = [i in range(startVal, endVal + GetMode(startVal, endVal), GetMode(startVal, endVal))]
        # Capture Only Start and End
        if inputJSON["type"] == "BNA":
            listToCapture.append(startVal)
            listToCapture.append(endVal)
        totalPad = int(math.ceil(math.log10(max(startVal, endVal))))
        currentImageType = helper.imageTypeMap[helper.ImageType[inputJSON["image_type"]]]        
        print(listToCapture)
        
        
        
        # Click and Create image
        for i in range(startVal, endVal + (-1) * GetMode(startVal, endVal), (-1) * GetMode(startVal, endVal)):
            # Click
            print("Current Step is {}".format(str(i)))
            helper.ClickAndWait(stepX, stepY, helper.SMALL_PAUSE)
            # Skip the ones that are not necessary
            if i not in listToCapture:
                continue
            print("Snapshot Step is {}".format(str(i)))
            # Create image
            pyautogui.screenshot(TIMELAPSE_IMAGE_NAME + str(i).zfill(totalPad) + currentImageType, region = imageRegion)
            
            
        # Make the video if needed
        if "video" in inputJSON:
            videoJSON = inputJSON["video"]
            videoName = DEFAULT_VIDEO_NAME
            videoFPS = DEFAULT_VIDEO_FPS
            videoCODEC = DEFAULT_VIDEO_CODEC
            if "name" in videoJSON:
                videoName = videoJSON["name"]
            if "codec" in videoJSON:
                videoCODEC = videoJSON["codec"]
            if "fps" in videoJSON:
                videoFPS = videoJSON["fps"]
            videoCreator.CreateVideo("./", videoName, currentImageType, videoCODEC, videoFPS)
            
        
        # Delete the images
        if inputJSON["type"] == "TIMELAPSE":
            for fileName in os.listdir('./'):
                if fileName.endswith(currentImageType):
                    os.remove(fileName)
                
        # Close Time Lapse
        helper.ClickAndWait(x, y)
            
        
            
            
        
        
    
    
    
    