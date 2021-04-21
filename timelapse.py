import pyautogui
import math
import os

import helper
import videoCreator


# this will have to be determined based on the device
backwardDelta = [-450, 150]
forwardDelta = [220, 150]
imageRegion = (590, 170,2600, 1420) 



TIMELAPSE_IMAGE_NAME = "timelapse_"
DEFAULT_VIDEO_NAME = "video"
DEFAULT_VIDEO_CODEC = "MP4V"
DEFAULT_VIDEO_FPS = 3


def record(inputJSON):
    helper.PauseForEffect(helper.SMALL_PAUSE)
    assert "start_count" in inputJSON, "Need to Specify start count"
    assert "end_count" in inputJSON, "Need to Specify end count"
    assert "mode" in inputJSON, "Need to specify the mode of the timelapse (FORWARD or BACKWARD)"
    assert "image_type" in inputJSON, "Need to Specify Image type for snapshot"
    
    # Locate Time Lapse
    x, y = helper.LocateImage('./common/timelapse.png')
    if x != None and y != None:
        # Start Time Lapse
        helper.ClickAndWait(x, y, helper.SMALL_PAUSE)
        startVal = inputJSON["start_count"]
        endVal = inputJSON["end_count"]
        steps = startVal - endVal
        # When it starts it starts at the Start
        # So if we need forward we need to hit back
        if inputJSON["mode"] == "FORWARD":
            for i in range(0, steps + 1): # Need Extra as we are taking a snapshot after click
                helper.ClickAndWait(x + backwardDelta[0], y + backwardDelta[1])
                

        # Preprocessing before taking snapshot
        stepX = x
        stepY = y
        if inputJSON["mode"] == "BACKWARD":
            stepX = x + backwardDelta[0]
            stepY = y + backwardDelta[1]
        if inputJSON["mode"] == "FORWARD":
            stepX = x + forwardDelta[0]
            stepY = y + forwardDelta[1]
        totalPad = int(math.ceil(math.log10(steps)))
        currentImageType = helper.imageTypeMap[helper.ImageType[inputJSON["image_type"]]]
        
        
        # Click and Create image
        for i in range(0, steps):
            # Click
            helper.ClickAndWait(stepX, stepY, helper.SMALL_PAUSE)
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
        for fileName in os.listdir('./'):
            if fileName.endswith(currentImageType):
                os.remove(fileName)
                
        # Close Time Lapse
        helper.ClickAndWait(x, y)
            
        
            
            
        
        
    
    
    
    