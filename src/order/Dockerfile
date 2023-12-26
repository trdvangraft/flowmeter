FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY wsgi.py wsgi.py
COPY config.py config.py
COPY ./src ./src
# COPY ../shared .


RUN groupadd -r order && useradd --no-log-init -r -g order order
USER order

EXPOSE 9600

CMD ["python",  "wsgi.py"]