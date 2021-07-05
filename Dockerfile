# syntax=docker/dockerfile:1
# Base docker file
FROM ubuntu:20.10

RUN apt-get dist-upgrade -y
RUN apt-get update

RUN apt update
RUN apt install software-properties-common -y


RUN apt-get dist-upgrade -y
RUN apt-get install python3-pip -y
RUN apt update

EXPOSE 8888
EXPOSE 8000

