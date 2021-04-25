import cv2
import numpy as np
import glob
import helper

def CreateVideo(folderPath, videoName, currentImageType, videoCODEC, videoFPS):
    videoExtension = helper.videoExtensionMap[helper.VideoCodec[videoCODEC]]
    videoName += videoExtension
    img_array = []
    for filename in sorted(glob.glob(folderPath + "/*" + currentImageType), reverse = True):
        print(filename)
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)

    print("Total Images : {} - {}".format(len(img_array), videoName))

    fourcc = cv2.VideoWriter_fourcc(*videoCODEC)
    out = cv2.VideoWriter(videoName, fourcc, videoFPS, size)
     
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()