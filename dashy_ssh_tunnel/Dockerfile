FROM alpine:3.11

COPY ./ssh /ssh
RUN apk add --no-cache \
  openssh-client \
  ca-certificates \
  bash &&\
  chmod -R 600 /ssh 
CMD ["ssh", "-i", "/ssh/id_rsa", "-o", "StrictHostKeyChecking=no", "-p", "2222", "-R", "dash:80:localhost:10810", "lt.bend.ovh"]
