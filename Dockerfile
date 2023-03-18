FROM python:3.10-slim-buster

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && \
    apt-get -y install gcc && \
    pip3 install uwsgi && \
    pip3 install -r requirements.txt && \
    apt-get -y remove gcc && \
    apt-get -y autoremove && \
    rm -rf /var/lib/apt/lists/*

COPY . .
EXPOSE 4000

CMD ["uwsgi", "--ini", "uwsgi.ini"]
