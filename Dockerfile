FROM quay.io/centos/centos:stream8 as arcaflow-elasticsearch-plugin

RUN dnf -y module install python39 && dnf -y install python39 python39-pip git
RUN mkdir /app

ADD https://raw.githubusercontent.com/arcalot/arcaflow-plugins/main/LICENSE /app
COPY es_plugin.py /app
COPY es_schema.py /app
COPY requirements.txt /app
WORKDIR /app

RUN pip3 install -r requirements.txt

# Test stage
FROM arcaflow-elasticsearch-plugin as test

COPY tests/unit/test_es_plugin.py /app

RUN pip3 install coverage
RUN python3 -m coverage run test_es_plugin.py

RUN mkdir /htmlcov
RUN python3 -m coverage html -d /htmlcov

FROM arcaflow-elasticsearch-plugin
ENTRYPOINT ["python3", "/app/es_plugin.py"]
CMD []

LABEL org.opencontainers.image.source="https://github.com/arcalot/arcaflow-plugin-elasticsearch"
LABEL org.opencontainers.image.licenses="Apache-2.0+GPL-2.0-only"
LABEL org.opencontainers.image.vendor="Arcalot project"
LABEL org.opencontainers.image.authors="Arcalot contributors"
LABEL org.opencontainers.image.title="Python Elasticsearch Plugin"
LABEL io.github.arcalot.arcaflow.plugin.version="1"