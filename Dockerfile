FROM selenium/standalone-firefox
FROM python:3.12-slim

RUN apt-get update && apt-get install firefox-esr wget -y

RUN /bin/bash -c 'set -ex && \
    ARCH=`uname -m` && \
    if [ "$ARCH" == "aarch64" ]; then \
        wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux-aarch64.tar.gz; \
        tar -xzvf geckodriver-v0.35.0-linux-aarch64.tar.gz -C /usr/local/bin; \
        chmod +x /usr/local/bin/geckodriver; \
        rm -rf geckodriver-v0.35.0-linux-aarch64.tar.gz; \
    fi'

COPY main.py pyproject.toml /
COPY /bearification /bearification
RUN pip install .

ENTRYPOINT ["python3", "-u", "main.py"]
