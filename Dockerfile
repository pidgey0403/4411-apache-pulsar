FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install pulsar-client

CMD ["python", "consumer.py", "&", "python", "producer.py"]