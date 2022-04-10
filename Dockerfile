FROM ubuntu:18.04

ENV GIT_SSL_NO_VERIFY=1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# apt install
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
         curl \
         git \
         gnupg2 \
         python3.8 \
         python3-pip \
         unzip \
         vim \
         wget

# copy src
RUN mkdir -p /opt/flaskbook_api
#COPY flaskbook_api/api /opt/flaskbook_api/api
COPY flaskbook_api/run.py /opt/flaskbook_api/run.py

# pip install
COPY requirements.txt /tmp/
RUN pip3 install --upgrade pip && \
    pip3 install -r /tmp/requirements.txt

# cd
WORKDIR /opt/flaskbook_api

# set env for flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV APPLICATION_SETTINGS=api/config/local.py

# expose port for flask
EXPOSE 5000

# flask run
CMD ["flask", "run", "-h", "0.0.0.0"]