FROM python:3.7

RUN apt-get update && apt-get install -y binutils patchelf upx && rm -rf /var/lib/apt/lists/*
RUN pip3 install staticx pyinstaller jinja2

COPY build.sh /app/
RUN chmod +x /app/build.sh

COPY setup.* /app/
COPY README.md /app
COPY tests /app/tests
COPY j2tmpl /app/j2tmpl

WORKDIR /app

ENTRYPOINT [ "/app/build.sh" ]
CMD [ "build" ]
