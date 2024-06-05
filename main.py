import cv2
import numpy as np
import autopy
import handtracking as htm
import time
import pyautogui as pg
import keyboard
import presentation  # Import the presentation module

# Define the slow_scroll function for continuous, smooth, and fast scrolling
def slow_scroll(px):
    if px > 0:
        for i in range(int(px)):
            pg.scroll(-30)
            time.sleep(0.004)
    else:
        for i in range(int(px) * -1):
            pg.scroll(30)
            time.sleep(0.004)

# Size the webcam
wcam, hcam = 680, 400
frameR = 100  # Frame Reduction

# Previous and Current location variables for smoothing
plocx, plocy = 0, 0
clocx, clocy = 0, 0
smoothning = 7

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
pTime = 0

# Initialize hand detector
detector = htm.handDetector(maxHands=1)

# Get screen size
wscr, hscr = autopy.screen.size()

dragging = False  # Variable to track dragging state

# Presentation mode flag
presentation_mode = False

while True:
    # Toggle presentation mode when 'p' or 'o' key is pressed
    if keyboard.is_pressed('p'):
        presentation_mode = True
        presentation.presentation_control.start_presentation()
    elif keyboard.is_pressed('o'):
        presentation_mode = False
        presentation.presentation_control.stop_presentation()
        pg.hotkey('win', 'down')  # Minimize PowerPoint window
    elif keyboard.is_pressed('esc'):
        break

    if presentation_mode:
        # 1. Find the hand landmarks
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)

        if len(lmList) != 0:
            # Get the tip positions of fingers
            x_index, y_index = lmList[8][1:]  # Index finger tip
            x_middle, y_middle = lmList[12][1:]  # Middle finger tip
            x_thumb, y_thumb = lmList[4][1:]  # Thumb tip
            x_pinky, y_pinky = lmList[20][1:]  # Pinky finger tip

            # Check which fingers are up
            fingers = detector.fingersUp()

            # Perform actions based on finger positions
            if fingers[4] == 1:
                presentation.presentation_control.next_slide()
                time.sleep(0.50)

            if fingers[1] == 1:
                presentation.presentation_control.previous_slide()
                time.sleep(0.50)

        # Frame rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # Display
        cv2.imshow("Presentation Mode", img)
    else:
        # 1. Find the hand landmarks
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]  # Index finger tip
            x2, y2 = lmList[12][1:]  # Middle finger tip
            x_thumb, y_thumb = lmList[4][1:]  # Thumb tip

            # Check which fingers are up
            fingers = detector.fingersUp()

            # Only index finger is up - Moving mode
            cv2.rectangle(img, (frameR, frameR), ((wcam - frameR), (hcam - frameR)), (255, 23, 14), 2)
            if fingers[1] == 1 and fingers[2] == 0:
                x3 = np.interp(x1, (frameR, wcam - frameR), (0, wscr))
                y3 = np.interp(y1, (frameR, hcam - frameR), (0, hscr))
                
                clocx = plocx + (x3 - plocx) / smoothning
                clocy = plocy + (y3 - plocy) / smoothning
                
                autopy.mouse.move(wscr - clocx, clocy)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocx, plocy = clocx, clocy
                
            # Both index and middle fingers are up - Clicking mode
            if fingers[1] == 1 and fingers[2] == 1:
                length, img, lineInfo = detector.findDistance(8, 12, img)

                if length < 30:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    pg.leftClick()
                    cv2.waitKey(500)

            # Right Click
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                pg.rightClick()
                cv2.waitKey(500)
        
            # Drag and Drop
            if not any(fingers):
                if not dragging:
                    pg.mouseDown()
                    dragging = True
                else:
                    x3 = np.interp(x1, (frameR, wcam - frameR), (0, wscr))
                    y3 = np.interp(y1, (frameR, hcam - frameR), (0, hscr))
                    clocx = plocx + (x3 - plocx) / smoothning
                    clocy = plocy + (y3 - plocy) / smoothning
                    autopy.mouse.move(wscr - clocx, clocy)
                    plocx, plocy = clocx, clocy
            else:
                if dragging:
                    pg.mouseUp()
                    dragging = False

            # Double Click
            if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                pg.doubleClick()
                cv2.waitKey(500)

            # Mouse wheel control
            if fingers[1] == 1 and fingers[2] == 1 and fingers[4] == 1 and fingers[0] == 0:
                if fingers[3] == 0:
                    slow_scroll(-30)  # Scroll up
                elif fingers[3] == 1:
                    slow_scroll(30)  # Scroll

        # Frame rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # Display
        cv2.imshow("Handless Navigation System", img)

    # Quit when 'Esc' is pressed
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
