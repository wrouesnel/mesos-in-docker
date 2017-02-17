# Build mesos for demos

FROM ubuntu:yakkety

RUN apt-get update && apt-get install -y build-essential git libcurl4-nss-dev \
    libsasl2-dev autoconf libtool zlib1g-dev libapr1-dev libsvn-dev cmake jq \
    default-jdk python-dev

RUN git clone https://git-wip-us.apache.org/repos/asf/mesos.git mesos-src
    
RUN cd mesos-src && \
    ./bootstrap && \
    ./configure CFLAGS=-g CXXFLAGS=-g --disable-java --disable-python && \
    ./config.status && \
    make -j3 && \
    make install

RUN mkdir -p /etc/mesos-agent /var/lib/mesos


