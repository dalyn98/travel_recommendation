# ubuntu:18.04

FROM pytorch/pytorch:latest

ENV DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update -y && apt-get install -y tzdata
RUN apt-get install -y python3.9.13
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9.13
RUN conda update -y conda && conda install -y airflow 

RUN airflow db init

RUN echo 'export AIRFLOW_HOME=~/airflow' >> /home/jovyan/.profile
RUN echo 'export AIRFLOW_HOME=~/airflow' >> /home/jovyan/.bashrc
RUN source ~/.profile
RUN mkdir $AIRFLOW_HOME/dags

RUN airflow users create --username admin --firstname KIM --lastname hyunwoo --role Admin --password admin --email dalyn8690@gmail.com

EXPOSE 80
