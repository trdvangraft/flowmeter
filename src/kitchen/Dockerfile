FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./src ./src
# COPY ../shared .


RUN groupadd -r kitchen && useradd --no-log-init -r -g kitchen kitchen
USER kitchen

EXPOSE 9600

CMD ["python",  "./src/app.py"]