FROM python:3.13.1
RUN apt update; apt install netcat-traditional

RUN python3 -m pip install pip --upgrade

RUN mkdir -p /usr/src_run_config/
WORKDIR /usr/src_run_config/

COPY ./requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r ./requirements.txt

WORKDIR /usr/src/
COPY ./tg_bot ./
