# pull official base image
FROM python:3.8.0-alpine

# set work directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip

# copy project
COPY . .
RUN pip install -r requirements.txt

RUN mv wait-for /bin/wait-for
RUN chmod +x /bin/wait-for
