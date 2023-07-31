FROM nvidia/cuda:8.0-devel-ubuntu16.04

RUN apt-get update -y
RUN apt-get install -y libopenblas-dev python-numpy python-dev swig git python-pip wget

COPY . /code
WORKDIR /code
ENV PYTHONPATH /code

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
