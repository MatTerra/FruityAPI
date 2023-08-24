FROM debian:12 AS build-uwsgi
RUN apt-get update && \
    apt-get -y install build-essential wget python3-dev libpcre3 libpcre3-dev && \
    wget https://files.pythonhosted.org/packages/b3/8e/b4fb9f793745afd6afcc0d2443d5626132e5d3540de98f28a8b8f5c753f9/uwsgi-2.0.21.tar.gz && \
    tar zxvf uwsgi-2.0.21.tar.gz && \
    cd uwsgi-2.0.21 && \
    make PYTHON=python3 && \
    mv uwsgi /usr/bin && cd .. && rm -rf uwsgi-2.0.21

FROM python:3.11 AS build-env
RUN mkdir /install
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install -I --prefix=/install --no-cache-dir -r requirements.txt && rm requirements.txt

FROM cgr.dev/chainguard/python:latest-dev
USER nonroot
ENV PROCESSES 1
ENV PORT 8080
ENV THREAD 1
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages:/app
EXPOSE 8080
COPY src/ /app
COPY --chown=nonroot:nonroot wsgi.ini /app/wsgi.ini
COPY --from=build-env /install /usr/local
COPY --from=build-uwsgi /usr/bin/uwsgi /app/uwsgi
COPY --from=build-uwsgi /usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0 /usr/lib/x86_64-linux-gnu/libpython3.11.so.1.0
WORKDIR /app
ENTRYPOINT ["/app/uwsgi", "--ini", "/app/wsgi.ini"]
