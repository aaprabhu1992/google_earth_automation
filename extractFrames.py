import cv2
import argparse
import math

def WriteImage(i, zFillVal, frame, method):
    h, w = frame.shape[:2]
    width_start = int(w/4)
    final_width = int(w/2)
    if method == 1:
        print("Shortening Image")
        frame = frame[:, width_start: width_start+final_width]
    cv2.imwrite('extracted_slice_'+str(i).zfill(zFillVal)+'.jpg',frame)

parser = argparse.ArgumentParser()
parser.add_argument('-name',
                    type=str,
                    help='Video file Name')
parser.add_argument('-frames',
                    nargs ="+",
                    help='Frame Numbers to be extracted')
parser.add_argument('-typeVal',
                    type=int,
                    help='Type of Frame Extraction')
args = parser.parse_args()
videoName = args.name
framesList = [int(x) for x in args.frames]
method = args.typeVal

zFillVal = int(math.ceil(max(framesList)))

# Opens the Video file
cap= cv2.VideoCapture(videoName)
i=0
prevFrame = None
while(cap.isOpened()):
    
    ret, frame = cap.read()
    if ret == False:
        break
    if i in framesList:
        WriteImage(i, zFillVal, frame, method)
    i+=1
    prevFrame = frame


if -1 in framesList:
    WriteImage(i, zFillVal, prevFrame, method)


cap.release()
cv2.destroyAllWindows()