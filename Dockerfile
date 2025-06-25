FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt app.py ./

RUN apt-get update && apt-get install -y curl
RUN pip install --no-cache-dir -r requirements.txt && \
    mkdir -p /app/data

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

EXPOSE 8080

CMD ["python", "app.py"]