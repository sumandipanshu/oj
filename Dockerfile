FROM alpine:latest
COPY ./ /checker
RUN apk add python3 pip3 && pip3 install -r requirements.txt
WORKDIR checker
