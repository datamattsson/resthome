FROM python:2.7-alpine
MAINTAINER michael.mattsson@gmail.com

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY resthome.py /usr/src/app/
COPY smartthings.json /usr/src/app/
ADD https://raw.githubusercontent.com/dpjanes/iotdb-smartthings/master/smartthings.py /usr/src/app

CMD [ "python2", "./resthome.py" ]
