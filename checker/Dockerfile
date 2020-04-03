FROM alpine:latest 
COPY ./ /checker
WORKDIR /checker
RUN ls -la /checker
RUN apk add python3 g++ gcc && pip3 install -r requirements.txt
