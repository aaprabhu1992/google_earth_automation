import pyautogui
import argparse

import helper

imageSnapRegion = (590, 170,2600, 1420) 

parser = argparse.ArgumentParser()
parser.add_argument('-name',
                    type=str,
                    help='Image file Name')
parser.add_argument('-imgType',
                    type=str,
                    help='imageType')
parser.add_argument('-wait',
                   type=str,
                   help='Time to wait before taking snap')
                   
args = parser.parse_args()
imageName = args.name
imageType = args.imgType
wait = args.wait

imageType = helper.imageTypeMap[helper.ImageType[imageType]]   
helper.PauseForEffect(int(wait))
helper.Beep()
pyautogui.screenshot(imageName + imageType, region = imageSnapRegion)
helper.Beep()
