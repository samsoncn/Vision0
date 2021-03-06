import cv2

cap = cv2.VideoCapture('./testing/t1.mp4')

frameTime = 50 

while (cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(frameTime) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()