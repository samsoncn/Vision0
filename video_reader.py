import cv2
from detect import detector

cap = cv2.VideoCapture('./testing/video.mp4')

frameTime = 10

while (cap.isOpened()):
    ret, frame = cap.read()
    frame = detector(frame)

    if cv2.waitKey(frameTime) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()