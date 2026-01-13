
FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /app

COPY . /app

RUN pip install psutil psycopg2-binary

# Comando que se ejecuta cuando prendes el contenedor
CMD ["python", "pyt.py"]