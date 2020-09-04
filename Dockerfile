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

RUN apk update                             \
 && apk install -y --no-install-recommends \
    ca-certificates curl firefox               \
 && rm -fr /var/lib/apt/lists/*                \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz | tar xz -C /usr/local/bin \
 && apk purge -y ca-certificates curl


# install dependencies
RUN pip install --upgrade pip

# copy project
COPY . .
RUN pip install -r requirements.txt

RUN mv wait-for /bin/wait-for
RUN chmod +x /bin/wait-for
