import cv2
import mediapipe as mp
import time
import numpy as np
import os
import HandTrackingModule as htm

#####
brush_thickness = 10
eraser_thickness = 80
cap = cv2.VideoCapture(0)
#####

# images
folder_path = 'header'
my_list = os.listdir(folder_path)
print(my_list)

overlay_list = []
for im_path in my_list:
    image = cv2.imread(f'{folder_path}/{im_path}')
    overlay_list.append(image)

print(len(overlay_list))

header = overlay_list[0]
# red
draw_colour = (0,0,255)
# green
#0,255,0
# yellow
#0,255,255


#url = "http://172.20.10.2:8080/video"
# cap = cv2.VideoCapture(url)

"""while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('IP Webcam Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
"""



########
# reframing scales
def rescaleFrames(frame,scale):
    width = int(frame.shape[1] * scale) # 1 is for width
    height = int(frame.shape[0] * scale) # 0 is for height
    dimensions = (width,height)

    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

#resized_image = rescaleFrames(img)

##########



cap.set(3,1280)
cap.set(4,720)

detector = htm.handDetector(detectionCon=0.85)
# first finger postion
xp,yp= 0,0
# image canvas
img_canvas = np.zeros((720,1280,3),np.uint8)
cv2.putText(img_canvas, 'Team: 1',(69,699), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
cv2.putText(img_canvas, 'Literary & Debate Club', (800, 699), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)



pTime = 0
cTime = 0

while True:
    # displaying the fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # 1. import image
    success, img = cap.read()
    img = cv2.flip(img,1)
    # reducing resolution


    # 2. find hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    cv2.putText(img, str(int(fps)), (1200, 699), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(img, 'Team: 1',(69,699), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    if len(lmList) != 0:
        #print(lmList)

        # tip of index and middle finger
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

        # 3. check which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)

        # 4. if selection mode is enabled - 2 fingers are up
        if fingers[1] and fingers[2] and fingers[3]==False:
            print('Selection Mode')
            xp, yp = 0, 0

            #checking if we are on top of the image of selection
            if y1 < 102:
                if 300 < x1 < 430: # red
                    header = overlay_list[0]
                    draw_colour = (0,0,255)
                elif 630 < x1 < 720: # yellow
                    header = overlay_list[1]
                    draw_colour = (0,255,255)
                elif 900 < x1 < 1020: # green
                    header = overlay_list[2]
                    draw_colour = (0,255,0)
                elif 1150 < x1 < 1255: # eraser
                    header = overlay_list[3]
                    draw_colour = (0,0,0)
            cv2.rectangle(img,(x1,y1-20), (x2,y2+20), draw_colour, cv2.FILLED)

        # 5. if the drawing mode - index finger is up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1), 15, draw_colour, cv2.FILLED)
            print('Drawing Mode')
            if xp ==0 and yp==0:
                xp,yp = x1,y1

            if draw_colour == (0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), draw_colour, eraser_thickness)
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_colour, eraser_thickness)
            else:
                cv2.line(img, (xp,yp), (x1,y1), draw_colour, brush_thickness)
                cv2.line(img_canvas, (xp,yp), (x1,y1), draw_colour, brush_thickness)

            #prev postition tracking
            xp,yp = x1,y1

        # direct eraser
        if fingers[1] and fingers[2] and fingers[3]:
            header = overlay_list[3]
            if xp ==0 and yp==0:
                xp,yp = x1,y1
            draw_colour = (0, 0, 0)
            cv2.circle(img,(x1,y1), 15, draw_colour, cv2.FILLED)
            print('eraser mode')
            #cv2.line(img, (xp, yp), (x1, y1), draw_colour, eraser_thickness)
            #cv2.line(img_canvas, (xp, yp), (x1, y1), draw_colour, eraser_thickness)

            xp, yp = x1, y1



    # resizing the header image
    header_resized = cv2.resize(header, (1280, 102))
    img[0:102, 0:1280] = header_resized
    img = cv2.addWeighted(img,0.7,img_canvas,0.8,0)

    #gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #scaling the screens
    img_rescaled = rescaleFrames(img,0.8)
    img_canvas_rescaled = rescaleFrames(img_canvas,0.45)
    cv2.imshow("image",img_rescaled)
    cv2.imshow("image_canvas",img_canvas_rescaled)
    cv2.waitKey(1)



