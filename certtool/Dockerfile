FROM golang:1.8

ADD https://github.com/wrouesnel/makecerts/releases/download/v0.1/makecerts /makecerts
RUN chmod +x /makecerts

ENTRYPOINT [ "/makecerts" ]
