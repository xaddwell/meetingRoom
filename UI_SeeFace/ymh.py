import cv2
import time


faceCascade = cv2.CascadeClassifier("weights/haarcascade_frontalface_alt2.xml")
img1 = cv2.imread('images/1.jpg')
img2 = cv2.resize(img1, dsize=(int(img1.shape[1] * 0.10), int(img1.shape[0] * 0.10)))
# start = time.time()
# for i in range(100):
#     # imgGray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#     face2 = faceCascade.detectMultiScale(img2, 1.2, 4)
#     for (x, y, w, h) in face2:
#         cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 2)
#     # cv2.imshow("Result2", img2)
#     # cv2.waitKey(0)
# end = time.time()
# print("time cost: ", end - start)
# # cv2.imshow("Result2", img2)
# # cv2.waitKey(0)
face2 = faceCascade.detectMultiScale(img2, 1.2, 4)
for (x, y, w, h) in face2:
    face = img2[y:y+h, x:x+w]
    face = cv2.resize(face, (face.shape[1] * 5, face.shape[0] * 5))
    cv2.imshow('face', face)

    cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 2)
cv2.imshow("Result2", img2)
cv2.waitKey(0)
cv2.destroyAllWindows()

