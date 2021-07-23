FROM alpine:latest
COPY ./ /oj 
WORKDIR oj
RUN apk add python3 g++ gcc && pip3 install -r requirements.txt
