FROM python:3.13-alpine
RUN apk add --update py3-pip
RUN pip install webdavclient3 
RUN mkdir /opt/app
COPY . /opt/app

WORKDIR /opt/app

CMD [ "python3", "-u", "/opt/app/run.py"]
