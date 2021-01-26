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

# MQTT Settings
MQTT_BROKER = os.getenv("MQTT_BROKER","54.215.95.106")
MQTT_TOPIC = os.getenv("MQTT_RECEIVE","w251/hw3")

# Save location for image locally
# TODO: Move to boto3 and send directly to S3
FILE_DIR = os.getenv("FILE_DIR","/mnt/w251")

# Image frame to use
frame = np.zeros((240, 320, 3), np.uint8)


def on_connect(client, userdata, flags, rc):
    """
    The callback for when the client receives a CONNACK response from the server.
    """
    print("Connected with result code "+str(rc))

    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    """
    The callback for when a PUBLISH message is received from the server.
    """
    global frame
    # Decoding the message
    img = base64.b64decode(msg.payload)

    # converting into numpy array from buffer
    npimg = np.frombuffer(img, dtype=np.uint8)

    # Convert to Frame
    frame = cv2.imdecode(npimg, 1)

    # Write out the image to the direction listed
    file_name = f"{time.time()}_{uuid.uuid1()}.jpeg"
    cv2.imwrite(f'{FILE_DIR}/{file_name}', frame)

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
