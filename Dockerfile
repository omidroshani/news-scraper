FROM ubuntu:latest


RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

ENV TZ=Asia/Tehran
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# set work directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update && apt-get install -y libpq-dev

# And of course we need Firefox if we actually want to *use* GeckoDriver
RUN apt-get update && apt-get install -y firefox wget

# Then install GeckoDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.27.0/geckodriver-v0.27.0-linux64.tar.gz
RUN tar -zxf geckodriver-v0.27.0-linux64.tar.gz -C /usr/bin
RUN geckodriver --version

# copy project
COPY . .
RUN pip3 install -r requirements.txt

RUN mv wait-for /bin/wait-for
RUN chmod +x /bin/wait-for
