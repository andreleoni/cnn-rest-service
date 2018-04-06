FROM andreleoni/cnn-tensorflow

MAINTAINER Andre Leoni <"andreluizleoni@gmail.com">

ENV LC_ALL C.UTF-8
ENV FLASK_APP flaskr
ENV FLASK_DEBUG true

COPY . /app

WORKDIR /app

RUN apt-get update \
    && apt-get install -y \
    git \
    vim \
    sqlite3

RUN pip3 install -r requirements.txt
RUN pip3 install --editable .
