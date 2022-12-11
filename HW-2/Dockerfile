FROM ubuntu:22.04

WORKDIR /work_directory

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y iputils-ping

COPY . .