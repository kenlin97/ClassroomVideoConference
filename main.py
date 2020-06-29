import numpy as np
import cv2
import dlib
import alert
import time
import math

cap = cv2.VideoCapture(0)
if cap.isOpened():
    width  = cap.get(3) # float
    height = cap.get(4) # float

halfwidth = int(width//2)
halfheight = int(height//2)
#print("width: " + str(width) + "  height: " + str(height))
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
count = 0
def handgesture(frame, width, height, kernel):
    half_height = int(height//2)
    half_width = int(width//2)
    roi = frame[half_height: int(height), half_width:int(width)]
    hls = cv2.cvtColor(roi, cv2.COLOR_BGR2HLS)  # converts the roi into HSV format
    lighter_thres = np.array([0, 25, 15], np.uint8)  # need a well lit room to work
    darker_thres = np.array([17, 200, 153], np.uint8)
    mask = cv2.inRange(hls, lighter_thres, darker_thres)  # filters to only see skin color
    #mask = cv2.medianBlur(mask, 9)  # blur the image
    mask = cv2.blur(mask, (12,12))
    ret, mask = cv2.threshold(mask, 150, 255, cv2.THRESH_BINARY)
    #mask = cv2.GaussianBlur(mask, (5, 5), 5)
    mask = cv2.dilate(mask, kernel, iterations=4)
    #mask = cv2.erode(mask, kernel, iterations=1)
    contour, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contour, key = lambda x: cv2.contourArea(x))
    perimeter = cv2.arcLength(max_contour, True)
    approx = cv2.approxPolyDP(max_contour, .0005*perimeter, True)
    hull = cv2.convexHull(max_contour)
    area_hull = cv2.contourArea(hull)
    area_contour = cv2.contourArea(max_contour)
    area_ratio = ((area_hull-area_contour)/area_contour*100)
    hull = cv2.convexHull(approx, returnPoints = False)
    defects = cv2.convexityDefects(approx, hull)
    l = 0

    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(approx[s][0])
        end = tuple(approx[e][0])
        far = tuple(approx[f][0])
        pt = (100, 180)

        # find length of all sides of triangle
        a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
        c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
        s = (a + b + c) / 2
        ar = math.sqrt(s * (s - a) * (s - b) * (s - c))

        # distance between point and convex hull
        d = (2 * ar) / a

        # apply cosine rule here
        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

        # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
        if angle <= 90 and d > 30:
            l += 1
            cv2.circle(roi, far, 3, [255, 0, 0], -1)

        # draw lines around hand
        #cv2.line(roi, start, end, [0, 255, 0], 2)
        center = cv2.moments(max_contour)
        x, y, w, h = cv2.boundingRect(max_contour)
        new_x = x + half_width
        new_y = y + half_height
        #cv2.rectangle(frame, (new_x, new_y), (new_x + w, new_y + h), (0, 255, 0), 2)

        cX = int(center["m10"] / center["m00"]) + half_width
        cY = int(center["m01"] / center["m00"]) + half_height

        #cv2.circle(frame, (cX, cY), 3, (0, 0, 255), -1)
        upper_distance = abs(cY - new_y)
        lower_distance = abs((new_y + h) - cY)

    l+=1

    #print(area_contour)
    if l==1:
        if area_ratio < 35 and area_ratio >= 20 and area_contour > 9000 and area_contour < 12000:
            if upper_distance < lower_distance:
                cv2.rectangle(frame, (20, 20), (int(width) - 20, int(height) - 20), (0, 0, 255), 10)
            else:
                cv2.rectangle(frame, (20, 20), (int(width) - 20, int(height) - 20), (0, 255, 0), 10)

    return mask

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    kernel = np.ones((3,3), np.uint8)
    # always use gray for processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    right_roi = frame[0:halfheight - 40, halfwidth+40:int(width)]  # defines region of interest to everything right and above the chin
    hsv = cv2.cvtColor(right_roi, cv2.COLOR_BGR2HSV) #converts the roi into HSV format
    lighter_thres = np.array([0, 10, 60], np.uint8) #need a well lit room to work
    darker_thres = np.array([15, 150, 255], np.uint8)
    mask = cv2.inRange(hsv, lighter_thres, darker_thres) #filters to only see skin color
    mask = cv2.medianBlur(mask, 7) # blur the image
    #mask = cv2.GaussianBlur(mask, (11, 11), 100)
    mask = cv2.dilate(mask, kernel, iterations = 4)
    contour, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(contour)
    hand_mask = handgesture(frame, width, height, kernel)

    for i in contour:
        x,y,w,h = cv2.boundingRect(i)
        rect_area = w*h
        if rect_area > 13000:
            cv2.rectangle(frame, (20, 20), (int(width) - 20, int(height) - 20), (0, 255, 255), 10)
            #print("Found the hand")

    #cv2.drawContours(frame, contour, -1, (0, 255, 0), 10)

    faces = detector(gray)

    #print(faces) # prints rectangles
    #to extract coordinates of face
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        landmarks = predictor(gray, face)
        upperY1 = landmarks.part(37).y
        upperX1 = landmarks.part(37).x
        lowerY1 = landmarks.part(41).y
        lowerX1 = landmarks.part(41).x
        upperY2 = landmarks.part(38).y
        upperX2 = landmarks.part(38).x
        lowerX2 = landmarks.part(40).x
        lowerY2 = landmarks.part(40).y
        leftX1 = landmarks.part(36).x
        rightX2 = landmarks.part(39).x

        '''
        difference1 = abs(upperY1 - lowerY1)
        print("left difference: " + str(difference1))
        difference2 = abs(upperY2 - lowerY2)
        print("right difference: " + str(difference2))
        '''
        #print(face)
        cv2.circle(frame,(upperX2, upperY2), 3,(0,255,0),1)
        cv2.circle(frame,(lowerX2, lowerY2), 3, (0, 0, 255), 1)
        cv2.circle(frame,(lowerX1, lowerY1), 3, (0, 0, 255), 1)
        cv2.circle(frame, (upperX1, upperY1), 3, (0, 255, 0), 1)

        EAR = (abs(upperY1 - lowerY1) + abs(upperY2 - lowerY2)) / (abs(leftX1 - rightX2))
        if EAR <= .7:
            count += 1
            if count > 50:
                print("HI")
                alert.alertuser()
                time.sleep(1)
                count = 0
        else:
            count = 0

        print("EAR: " + str(round(EAR, 2)) + "   count = " + str(count))
    # Display the resulting frame
    cv2.imshow('frame',frame)
    #cv2.imshow('mask', mask)
    #cv2.imshow('hand', hand_mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()