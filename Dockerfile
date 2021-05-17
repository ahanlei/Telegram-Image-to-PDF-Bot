FROM python:latest

ENV VIRTUAL_ENV "/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg opus-tools bpm-tools
RUN python -m pip install --upgrade pip

RUN git clone https://github.com/mastermindvrtx/Telegram-Image-to-PDF-Bot.git && \
    cd Telegram-Image-to-PDF-Bot && \
    pip3 install -U -r requirements.txt

WORKDIR /Telegram-Image-to-PDF-Bot
CMD python3 mastermindvrtx.py
