# Jhiciano - W251 - Spring 2021

WORKDIR:=$(shell pwd)

.PHONY: create-infra
docker-build-infra:
	@echo ${WORKDIR}
	@docker build -t w251-terraform:latest -f Dockerfile.terraform  .
	@docker run -i -t w251-terraform:latest

.PHONY: docker-build-mqtt
docker-build-mqtt:
	@docker build \
	-t w251_mqtt:latest \
	-f Dockerfile.mqtt .

.PHONY: docker-build-jetson
docker-build-jetson:
	@docker build \
	-t w251_jetson:latest \
	-f Dockerfile.jetson .

.PHONY: run-mqtt-sub
run-mqtt-sub:
	@docker run -it -v /mnt/w251:/mnt/w251 w251_jetson:latest python3 stream_reader.py

.PHONY: run-jetson
run-jetson:
	@docker run -it --device=/dev/video0:/dev/video0 w251_jetson:latest python3 stream.py