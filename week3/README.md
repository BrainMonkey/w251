# General

https://github.com/MIDS-scaling-up/v2/tree/master/week03/hw

Used Make file to build the containers and run the code. 

# Infrastructure

## Terraform

Use terraform to provison a EC2 instance and bucket.

### EC2 Instance

 IP Addrress: `54.215.95.106`
 Region: `us-west-1`

 ### S3 Bucket

Bucket: `berkeley-w251`
Region: `us-west-1`


# Docker

Use docker and docker-compose to create containers for services and deploy them to local host as well as AWS EC2 instance.

### MQTT Broker

Image: `hivemq/hivemq4`

Used all the defaults, with no volumes mounted.  Once the container is closed, all data is lost. 

#### Jetson - Cuda

Used a single container to stream in video from webcam connected to Jetson device. If a face is detected, the frame is sent to the desginated MQTT broker. 

#### MQTT Subscriber

This is a Python 3.9 base with packages and streaming code copied into it. 
