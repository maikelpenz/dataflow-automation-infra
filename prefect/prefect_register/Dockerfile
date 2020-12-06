# Container image that runs your code
FROM alpine:3.10
RUN apk update
RUN apk upgrade 
RUN apk add git
RUN apk add docker

# Set timezone
ENV TZ=UTC

# Install Python
RUN echo "**** install Python ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

# Install required packages for Prefect
RUN apk add gcc python3-dev build-base musl-dev libc-dev openssl-dev linux-headers

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh
COPY workflow_register.py /tmp/workflow_register.py
COPY action_helpers.py /tmp/action_helpers.py

# Code file to execute when the docker container starts up (`entrypoint.sh`).
ENTRYPOINT ["/entrypoint.sh"]