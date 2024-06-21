FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt update -y && apt upgrade -y
RUN apt install make -y && apt autoclean -y && apt autoremove -y
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r /app/requirements.txt

EXPOSE 8000
EXPOSE 5432