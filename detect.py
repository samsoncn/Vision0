import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
import imutils 

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

classifier_file = 'cars.xml'

car_tracker = cv2.CascadeClassifier(classifier_file)

def detector(frame):
    rect, weight = hog.detectMultiScale(frame, winStride=(6, 8), padding=(3, 3), scale=1.15)
    # rect, weight = hog.detectMultiScale(frame, winStride=(2, 6), padding=(6, 6), scale=2)

    cars = car_tracker.detectMultiScale(frame)

    rect = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rect])
    label = non_max_suppression(rect, probs=None, overlapThresh=0.65)
    
    c = 0
    for (x, y, w, h) in label:
        c += 1

        cv2.rectangle(frame, (x, y), (w, h), (139, 30, 90), 2)
        cv2.rectangle(frame, (x, y - 15), (w, y), (139, 30, 90), -1)
        cv2.putText(frame, f'Person{c}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y - 15), (x+w, y), (0, 0, 255), -1)
        cv2.putText(frame, f'Car{c}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow('Vision 0', frame)
    return frame, c
