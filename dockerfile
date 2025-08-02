FROM python:3.12-slim
EXPOSE 8000
WORKDIR /app

RUN apt update 
# A tool for merging audio and video streams:
RUN apt install -y ffmpeg  
# Tools to set up the MySQL connection:
RUN apt install -y build-essential
RUN apt install -y pkg-config
RUN apt install -y pkg-config libmariadb-dev
# Install dos2unix to ensure that the entrypoint file starts as expected
RUN apt install -y dos2unix
# Installing Cron for scheduling
RUN apt install -y cron
# NetCat to postpone the start of the app until the db is running
RUN apt install -y netcat-openbsd

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY cron/crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab

COPY entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]