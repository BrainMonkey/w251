####################################################################################
# Judge Hiciano
# Assignment 3
# Spring 2021 - W251
####################################################################################

# Importing Libraries
import base64
import os
import time

import cv2
import paho.mqtt.client as mqtt


# MQTT Broker Settings
MQTT_BROKER = "54.215.95.106"
MQTT_PORT = 1883
MQTT_TOPIC = "w251/hw3"

# OpenCV XML Classifer Data
FRONTALFACE_FILE_PATH = (
    os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_default.xml"
)
face_cascade = cv2.CascadeClassifier(FRONTALFACE_FILE_PATH)

# Creating OpenCV video capture object
cap = cv2.VideoCapture(0)

# Establishing MQTT connection with the Broker
client = mqtt.Client()
client.connect(MQTT_BROKER)

try:
    print("Starting Stream !!!!")
    while True:

        # Read Frame
        _, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # If a face is found, send it up to the cloud broker
        if len(faces):
            print("Face found")

            for (x, y, w, h) in faces:
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # Leaving in for future reference as working example to add eye dection as well
                # roi_gray = gray[y:y+h, x:x+w]
                # roi_color = frame[y:y+h, x:x+w]
                # eyes = eye_cascade.detectMultiScale(roi_gray)
                # for (ex,ey,ew,eh) in eyes:
                #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

            # Encoding the Frame
            _, buffer = cv2.imencode(".jpg", frame)
            # Converting into encoded bytes
            jpg_as_text = base64.b64encode(buffer)
            # Publishig the Frame on the Topic home/server
            client.publish(MQTT_TOPIC, jpg_as_text)


except:
    cap.release()
    client.disconnect()
    print("\nNow you can restart fresh")
