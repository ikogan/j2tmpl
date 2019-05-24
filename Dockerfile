FROM python:3

COPY j2tmpl /app/j2tmpl
COPY tests /app/tests
COPY setup.* /app/
COPY build.sh /app

RUN chmod +x /app/build.sh

WORKDIR /app

ENTRYPOINT /app/build.sh