FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y wget
RUN rm -rf /var/lib/apt/lists/*

RUN wget https://fastdl.mongodb.org/tools/db/mongodb-database-tools-ubuntu2204-x86_64-100.10.0.deb -O /tmp/mongodb-tools.deb && \
    dpkg -i /tmp/mongodb-tools.deb && \
    rm /tmp/mongodb-tools.deb

WORKDIR /data

CMD ["bash"]
