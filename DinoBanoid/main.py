import cv2
import cvzone
import numpy as np
import pyautogui
from cvzone.FPS import FPS
from mss import mss


fpsReader = FPS()
def capture_screen_region_opencv(x,y,desired_width, desired_height):
    screenshot = pyautogui.screenshot(region=(x,y,desired_width,desired_height))
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot,cv2.COLOR_RGB2BGR)
    return screenshot

def game_logic(conFound,_imgContours, jump_distance= 1):
    if conFound:
        left_most_contour = sorted(conFound,key=lambda x:x["bbox"][0])
        print(left_most_contour[0]["bbox"][0])
        cv2.line(_imgContours,(0,left_most_contour[0]["bbox"][1]+10),
                 (left_most_contour[0]["bbox"][0],left_most_contour[0]["bbox"][1]+10),
                 (0,200,0),10
                 )

        if left_most_contour[0]["bbox"][0] < jump_distance:
            pyautogui.press("space")
            print("jump")
    return _imgContours


def pre_process(_imgCrop):
    gray_frame = cv2.cvtColor(_imgCrop,cv2.COLOR_BGR2GRAY)
    _, binary_frame = cv2.threshold(gray_frame,127,255,cv2.THRESH_BINARY_INV)
    cv2.imshow("binary frame",binary_frame)
    canny_frame = cv2.Canny(binary_frame,50,50)
    #cv2.imshow("Canny Frame",canny_frame)
    kernel=np.ones((5,5))
    dilated_frame =cv2.dilate(canny_frame,kernel,iterations=1)
    #cv2.imshow("dilated_frame",dilated_frame)
    return dilated_frame
def find_obstacles(_imgCrop,_imgPre):
    imgContours, conFound = cvzone.findContours(_imgCrop,_imgPre,minArea=100,filter=None)
    return imgContours, conFound

while True:
    imgGame=capture_screen_region_opencv(450,240,650,350)

    cp = 100,300,310
    imgCrop = imgGame[cp[0]:cp[1],cp[2]:]

    imgPre = pre_process(imgCrop)

    imgContours, conFound = find_obstacles(imgCrop,imgPre)

    fps, imgGame = fpsReader.update(imgGame)

    imgContours = game_logic(conFound,imgContours)


    imgGame[cp[0]:cp[1],cp[2]:] = imgContours


    cv2.imshow("Game",imgGame)
    #cv2.imshow("imgCrop",imgCrop)
    #cv2.imshow("imgContoru",imgContours)
    cv2.waitKey(1)