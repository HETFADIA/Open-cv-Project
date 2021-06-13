import cv2

cap=cv2.VideoCapture(0)

while 1:
    ret,frame=cap.read()
    if ret==True:
        cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break;
cap.release()
cv2.destroyAllWindows()
