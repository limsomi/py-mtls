# Dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    iproute2 iputils-ping netcat curl openssh-client

CMD [ "bash" ]
