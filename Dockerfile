FROM python:3.7

RUN apt-get update && apt-get install -y upx && rm -rf /var/lib/apt/lists/*
RUN pip3 install pyinstaller jinja2

COPY setup.* /app/
COPY build.sh /app
COPY j2tmpl /app/j2tmpl
COPY tests /app/tests

RUN chmod +x /app/build.sh

WORKDIR /app

ENTRYPOINT /app/build.sh