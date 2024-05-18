import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("C:/Users/hp/PycharmProjects/pythonProject/serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recognition-5bd76-default-rtdb.firebaseio.com/",
    'storageBucket': "face-recognition-5bd76.appspot.com"
})

# Import necessary libraries

# Initialize Firebase

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, 500)
cap.set(4, 300)

# Load background image
imgBackground = cv2.imread('resources/9.jpg')

# Load known encoded faces from file
print("loading encoded file")
file = open("encodeFile.p", 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds)
print("encoded file loaded")

# Initialize variables
id = -1
counter = 0

# Main loop
while True:
    success, img = cap.read()
    imgBackground[162:162 + 360, 55:55 + 640] = img

    # Resize and convert image
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Face detection and recognition
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    num_faces_detected = len(faceCurFrame)

    if num_faces_detected == 2:
        print("Two faces detected, closing the camera.")
        break

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print("matches", matches)
        print("faceDis", faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            print("known face detected")
            print(studentIds[matchIndex])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = x1, y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(img, bbox, rt=0)
            id = studentIds[matchIndex]
            if counter == 0:
                counter = 1
            if counter == 1:
                studentInfo = db.reference(f'Students/{id}').get()
                if studentInfo:
                    print(studentInfo)
                    # Overlay student name on the image
                    cv2.putText(imgBackground, str(studentInfo['Name']), (x1, y1 - 10),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

    cv2.imshow("face", imgBackground)


    cv2.waitKey(1)




# Release camera and close windows
cap.release()
cv2.destroyAllWindows()
