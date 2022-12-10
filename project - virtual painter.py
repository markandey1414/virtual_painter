'''Color detection, webcam and printing the color'''
# contouring is needed to find out the location at the current instant
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # defining the size of output screen
cap.set(4, 720)
cap.set(10, 100)    # brightness

myColors = [[54, 173, 28, 177, 255, 255]]
myColorValues = [[255, 0, 0]]

points = []     # [x, y, colorId]
# hue, saturation and value for 'blue' color


def findColor(img, myColors, myColorValues):
    newPoints = []
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array(myColors[0][0:3])
    upper = np.array(myColors[0][3:6])
    mask = cv2.inRange(imgHSV, lower, upper)
    x, y = getContours(mask)
    cv2.circle(imgResult, (x, y), 10, myColorValues[0], cv2.FILLED)
    if x!=0 and y!=0:
        newPoints.append([x, y, 0])
    #cv2.imshow("mask", mask)
    return newPoints
def getContours(img):
    countours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in countours:
        area = cv2.contourArea(cnt)
        if area>500:
            print(cnt)
            cv2.drawContours(imgResult, cnt, -1, (0, 255, 0), 2)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y

def Draw(points, myColorValues):
    for point in points:
        cv2.circle(imgResult, (point[0], point[1]), 15, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)


    if len(newPoints) != 0:
        for newP in newPoints:
            points.append(newP)

    if len(points) != 0:
        Draw(points, myColorValues)
    cv2.imshow("output", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):       # bitwise and
        break

