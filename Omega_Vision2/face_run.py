
# ### Train Model

# In[6]:

import cv2
import numpy as np
import time
import os
from os import listdir
from os.path import isfile, join






data_path = './faces/user/'
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]


Training_Data, Labels = [], []


for i, files in enumerate(onlyfiles):
    image_path = data_path + onlyfiles[i]
    images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    Training_Data.append(np.asarray(images, dtype=np.uint8))
    Labels.append(i)


Labels = np.asarray(Labels, dtype=np.int32)


model = cv2.face.createLBPHFaceRecognizer()



model.train(np.asarray(Training_Data), np.asarray(Labels))
print("Model trained sucessefully")


# ### Facial Recognition

# In[9]:

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_detector(img, size=0.5):


    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if faces is ():
        return img, []

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200, 200))
    return img, roi



cap = cv2.VideoCapture(0)


f_pr = 0
i = 0
co1 = 0
while True:
    global f
    f = 0
    ret, frame = cap.read()

    image, face = face_detector(frame)



    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        results = model.predict(face)

        if results[1] < 500:
            confidence = int( 100 * (1 - (results[1])/400) )
            display_string = str(confidence) + '% Confident it is a resident'

        cv2.putText(image, display_string, (50, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255,120,150), 2)

        if confidence > 75:
            f =1
            co1 = 0
            cv2.putText(image, "Hi Sree Vishnu", (175, 390), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            cv2.imshow('Face Recognition', image )
        else:
            cv2.putText(image, "Unrecognized resident", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
            cv2.imshow('Face Recognition', image )

    except:
        #cv2.putText(image, "Unrecognized resident", (150, 120) , cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        #cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        cv2.imshow('Face Recognition', image )
        pass


    if f == 1 and f_pr == 0:
        os.system("mosquitto_pub -h 192.168.43.114 -t recognize -m 'sree vishnu'")
        f_pr = 1
    elif f == 0:
        co1 = co1+1
        if co1 >=80:
            f_pr =0
            co1 = 0


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
