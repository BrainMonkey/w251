####################################################################################
# Judge Hiciano
# Assignment 3
# Spring 2021 - W251
####################################################################################

import base64
import os
import time
import uuid

import cv2
import numpy as np
import paho.mqtt.client as mqtt

MQTT_BROKER = os.getenv("MQTT_BROKER","54.215.95.106")
MQTT_TOPIC = os.getenv("MQTT_RECEIVE","w251/hw3")
FILE_DIR = os.getenv("FILE_DIR","/mnt/w251")

frame = np.zeros((240, 320, 3), np.uint8)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global frame
    # Decoding the message
    img = base64.b64decode(msg.payload)

    # converting into numpy array from buffer
    npimg = np.frombuffer(img, dtype=np.uint8)
    # Decode to Original Frame
    frame = cv2.imdecode(npimg, 1)
    cv2.imwrite(f'{FILE_DIR}/{time.time()}_{uuid.uuid1()}.jpeg', frame)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER)

# Starting thread which will receive the frames
client.loop_start()

while True:

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the Thread
client.loop_stop()
