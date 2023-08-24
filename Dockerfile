FROM python:3.11 AS build-env
RUN mkdir /install
RUN mkdir /app
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
COPY --from=build-env /install /usr/local
WORKDIR /app
CMD ["/usr/local/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
