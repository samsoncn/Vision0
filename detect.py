import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
# import nms


hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def detector(frame):
    rect, weight = hog.detectMultiScale(frame, winStride=(4,4), padding=(6, 6), scale=1.00)
    rect = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rect])
    label = non_max_suppression(rect, probs=None, overlapThresh=0.6)

    c = 1
    for x, y, w, h in label:
        cv2.rectangle(frame, (x, y), (w, h), (139, 34, 104), 2)
        cv2.rectangle(frame, (x, y - 20), (w, y), (139, 34, 104), -1)
        cv2.putText(frame, f'Person{c}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        c += 1

    # cv2.putText
    return frame

