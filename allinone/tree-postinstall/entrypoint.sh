#!/bin/bash

function log() {
    echo "$@"
}

function echoerr() {
    echo "$@" 1>&2
}

function genpassword() {
    echo $(pwgen 48 1)
}

function stdbool() {
    if [ -z "$1" ] ; then
        echo "n"
    else
        echo ${1:0:1} | tr [A-Z] [a-z]
    fi
}

if [ -z $HOSTNAME ] ; then
    HOSTNAME=$(hostname -f)
fi

export DATA_DIR=/data

mkdir -p $DATA_DIR
chmod 755 $DATA_DIR

log "Templating syslog-ng configuration..."
export SERVICES="$(ls -1 /etc/services | tr '\n' ' ')pdns-api nginx-access nginx-error"
p2 -t /etc/syslog-ng.conf.p2 -o /run/syslog-ng.conf || ( echoerr "Templating syslog-ng config failed." ; exit 1 )
chmod 644 /run/syslog-ng.conf

log "Create logging fifo directory"
mkdir -p /run/log

# This structure ensures we can CTRL+C on the desktop.
cp -af /etc/services /run/services
runsvdir /run/services &
PID=$!
trap "kill -TERM $PID" INT TERM
wait $PID
wait $PID
exit $?
