import cv2
import imutils
from detect import detector

cap = cv2.VideoCapture('./testing/video.mp4')

while (cap.isOpened()):
    ret, frame = cap.read()
    # print(frame)
    # print(fps)
    frame = imutils.resize(frame, width=min(800, frame.shape[1]))
    frame = detector(frame)

    # When user click 'enter', it will stop
    if cv2.waitKey(1) == 13:
        break
    if frame is None:
        break
    
cap.release()
cv2.destroyAllWindows()