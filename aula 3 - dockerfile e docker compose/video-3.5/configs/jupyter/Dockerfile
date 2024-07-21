FROM jupyter/base-notebook:x86_64-python-3.11.6

USER root

WORKDIR /home/jupyternb

ENV JUPYTER_TOKEN="token"
ENV CHOWN_HOME="yes"
ENV NB_USER="jupyternb"

RUN apt-get update && \
    apt-get install -y gcc

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

ENTRYPOINT ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''", "--port=8888"]

EXPOSE 8888