FROM python:3.7

RUN pip3 install j2tmpl

COPY entrypoint.sh /usr/local/bin/generate-config
RUN chmod +x /usr/local/bin/generate-config

ENTRYPOINT ["/usr/local/bin/generate-config"]
