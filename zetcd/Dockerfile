FROM golang:1.8

RUN go get -v github.com/coreos/zetcd && \
    go build -o /zetcd github.com/coreos/zetcd/cmd/zetcd
    
ENTRYPOINT [ "/zetcd" ]
