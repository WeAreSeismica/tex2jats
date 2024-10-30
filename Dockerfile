FROM pandoc/core:2.19

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache perl python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools beautifulsoup4 lxml git+https://github.com/WeAreSeismica/biblib

WORKDIR /data

COPY ./docker_entrypoint.sh /tmp/docker_entrypoint.sh

COPY ./tex2xml.sh /tmp/
COPY ./apa.csl /tmp/
COPY ./cleanjats.py /tmp/
COPY ./sort_bib.py /tmp/

ENTRYPOINT ["sh", "/tmp/docker_entrypoint.sh"]
