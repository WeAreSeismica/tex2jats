FROM pandoc/core:2.19

#ENV LATEX_DIR=
#ENV TEX_FILENAME=
#ENV BIB_FILENAME=

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache perl python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /data

COPY ./docker_entrypoint.sh /tmp/docker_entrypoint.sh

COPY ./tex2xml.sh /tmp/
COPY ./apa.csl /tmp/
COPY ./cleanidjats.py /tmp/
COPY ./cleanxrefjats.py /tmp/
COPY ./metatex2jats.py /tmp/

ENTRYPOINT ["sh", "/tmp/docker_entrypoint.sh"]