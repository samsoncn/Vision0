import cv2
from detect import detector

cap = cv2.VideoCapture('./testing/t3.mp4')

while (cap.isOpened()):
    ret, frame = cap.read()
    # print(frame)
    # print(fps)
    frame = detector(frame)

    if cv2.waitKey(1) == 13:
        break
    if frame is None:
        break
    
cap.release()
cv2.destroyAllWindows()