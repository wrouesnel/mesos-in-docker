# All-in-one Mesos/Marathon/Zookeeper container built from sources.
# Needs --privileged.
# Required Binds to work:
#    -v /var/run/docker.sock:/var/run/docker.sock
#    -v /usr/bin/docker:/usr/bin/docker:ro
#    -v /sys/fs/cgroup:/sys/fs/cgroup

ARG DOCKER_PREFIX=
FROM ${DOCKER_PREFIX}ubuntu:yakkety

ARG http_proxy=
ARG https_proxy=

ARG URL_P2CLI=https://github.com/wrouesnel/p2cli/releases/download/r5/p2

COPY *.asc /tmp

RUN apt-key add /tmp/*.asc && rm -f /tmp/*.asc

RUN apt-get update && apt-get install -y \
        apt-transport-https \
        sudo \
        wget \
        runit \
        syslog-ng-core \
        openssl \
        pwgen \
        curl \
        dnsutils \
        apache2-utils && \
    # Templating engine
    wget -O /usr/local/bin/p2 $URL_P2CLI && \
    chmod +x /usr/local/bin/p2

# Mesos build-deps
RUN apt-get update && apt-get install -y build-essential git libcurl4-nss-dev \
    libsasl2-dev autoconf libtool zlib1g-dev libapr1-dev libsvn-dev cmake jq \
    default-jdk python-dev

# Marathon build-deps
RUN echo "deb https://dl.bintray.com/sbt/debian /" | tee -a /etc/apt/sources.list.d/sbt.list && \
    apt-get update && apt-get install -y scala sbt

# Runtime deps
RUN apt-get update && apt-get install -y zookeeper zookeeper-bin runit

RUN git clone --depth=1 https://git-wip-us.apache.org/repos/asf/mesos.git mesos-src && \
    git clone --depth=1 https://github.com/mesosphere/marathon.git marathon-src

RUN apt-get update && apt-get install -y maven

# Build Mesos
RUN cd mesos-src && \
    ./bootstrap && \
    ./configure CFLAGS=-g CXXFLAGS=-g --disable-python && \
    ./config.status && \
    make && \
    make install
    
# Build Marathon
RUN cd marathon-src && \
    sbt universal:packageZipTarball && \
    mkdir -p /opt/marathon && \
    tar -xvzf target/universal/marathon*.tgz -C /opt/marathon --strip-components=1

RUN mkdir -p /etc/mesos-agent /var/lib/mesos

ENV SVDIR=/run/services

RUN apt-get update && apt-get install -y rsync net-tools iproute2

COPY tree-postinstall/ /

RUN rsync -av /etc/zookeeper/conf.replacements/ /etc/zookeeper/conf/ && \
    rm -rf /etc/zookeeper/conf.replacements/

RUN ldconfig

ENTRYPOINT [ "/entrypoint.sh" ]
