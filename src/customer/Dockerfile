FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY customer_service.py customer_service.py
# COPY ../shared .


RUN groupadd -r order && useradd --no-log-init -r -g order order
USER order

CMD ["python3",  "customer_service.py"]