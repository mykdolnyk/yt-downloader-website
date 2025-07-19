FROM python:3.12-slim
EXPOSE 8000
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt update && apt install -y ffmpeg

COPY . .

RUN python ytviewer/manage.py migrate

CMD [ "python", "ytviewer/manage.py", "runserver", "0.0.0.0:8000"]