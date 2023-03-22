FROM python:3.10-slim-buster

WORKDIR /app

COPY main.py .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

CMD ["python", "main.py"]

VOLUME ["app/IO"]