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



#CONSTANTS (Independent of the screen resolution)
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
    
    
def GetListToCapture(inputJSON, startVal, endVal):
    listToCapture = []
    # Capture All Steps
    if inputJSON["type"] == "TIMELAPSE":
        listToCapture = [i in range(startVal, endVal + GetMode(startVal, endVal), GetMode(startVal, endVal))]
    # Capture Only Start and End
    if inputJSON["type"] == "BNA":
        listToCapture.append(startVal)
        listToCapture.append(endVal)
    return listToCapture
    
    
def CreateVideoFromJSON(videoJSON):
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


def GoToStartPoint(startVal, endVal, x, y):
    count = 0
    # Need Extra as we are taking a snapshot after click
    # For FORWARD we should move 1 step ahead, hence range increases by 2
    # For BACKWARD we should  go 1 step behind, hence rnage should not increase
    for i in range(1, startVal + (1  + GetMode(startVal, endVal))): 
        helper.ClickAndWait(x + backwardDelta[0], y + backwardDelta[1])
        count += 1
    print("Total Clicks : {}".format(str(count)))
            
    helper.PauseForEffect(helper.MEDIUM_PAUSE)
    print("Current Mode is {}".format(str(GetMode(startVal, endVal))))


def CreateImages(startVal, endVal, stepX, stepY, listToCapture, imageName, imageNamePadding, imageType, imageSnapRegion):
    # Click and Create image
    for i in range(startVal, endVal + (-1) * GetMode(startVal, endVal), (-1) * GetMode(startVal, endVal)):
        helper.ClickAndWait(stepX, stepY, helper.SMALL_PAUSE)
        # Click
        print("Now on Click {}".format(str(i)))
        # Skip the ones that are not necessary
        if i not in listToCapture:
            continue
        if i < 0:
            continue
        print("Snapshot Click is {}".format(str(i)))
        # Create image
        pyautogui.screenshot(imageName + str(i).zfill(imageNamePadding) + imageType, region = imageSnapRegion)


def GetImageNameAndType(imageJSON):
    assert "image_type" in imageJSON
    imageType = helper.imageTypeMap[helper.ImageType[imageJSON["image_type"]]]   
    imageName = TIMELAPSE_IMAGE_NAME
    if "image_name" in imageJSON:
        imageName = imageJSON["image_name"]
    return imageName, imageType
    
def CheckJSONForCorrectness(inputJSON):
    assert "start_count" in inputJSON, "Need to Specify start count"
    assert "end_count" in inputJSON, "Need to Specify end count"
    assert "image" in inputJSON, "Image property has to be defined"

def record(inputJSON):
    helper.PauseForEffect(helper.SMALL_PAUSE)
    
    if "place" in inputJSON:
        GoToPlace(inputJSON["place"])
    if "scroll" in inputJSON:
        helper.LocateAndClick('./common/earth.png', helper.MEDIUM_PAUSE, adjY = centerOfPoint)
        for i in range(0,inputJSON["scroll"]):
            pyautogui.scroll(SCROLL_AMOUNT)

    
    # Locate Time Lapse
    x, y = helper.LocateImage('./common/timelapse.png')
    if x != None and y != None:
        # Start Time Lapse
        helper.ClickAndWait(x, y, helper.SMALL_PAUSE)
        startVal = inputJSON["start_count"]
        endVal = inputJSON["end_count"]
        assert startVal != endVal, "Start and End Cannot be the same"
        # When Imagery starts its on the actual date
        # At the current date there is not image
        # When you click BACK for the first time, it moves to the 
        # Latest Available Imagery / Image Ticker 0
        helper.ClickAndWait(x + backwardDelta[0], y + backwardDelta[1])
        GoToStartPoint(startVal, endVal, x, y)

        # Preprocessing before taking snapshot
        stepX = x
        stepY = y
        if GetMode(startVal, endVal) == -1:
            stepX = x + backwardDelta[0]
            stepY = y + backwardDelta[1]
        if GetMode(startVal, endVal) == 1:
            stepX = x + forwardDelta[0]
            stepY = y + forwardDelta[1]
        listToCapture = GetListToCapture(inputJSON, startVal, endVal)
        totalPad = int(math.ceil(math.log10(max(startVal, endVal))))
        imageName, imageType = GetImageNameAndType(inputJSON["image"])
        
        
        CreateImages(startVal, endVal, stepX, stepY, listToCapture, imageName, totalPad, imageType, imageRegion)
            
            
        # Make the video if needed
        if "video" in inputJSON:
            videoJSON = inputJSON["video"]
            CreateVideoFromJSON(videoJSON)
            
        
        # Delete the images
        if inputJSON["type"] == "TIMELAPSE":
            for fileName in os.listdir('./'):
                if fileName.endswith(imageType):
                    os.remove(fileName)
                
        # Close Time Lapse
        helper.ClickAndWait(x, y)
            
        
            
            
        
        
    
    
    
    