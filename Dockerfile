FROM python:3.6-alpine

RUN apk --no-cache add --virtual build-deps \
        musl-dev \
        linux-headers \
        zlib-dev \
        jpeg-dev=8-r6 \
        g++ \
        gcc \
    && pip install cython

COPY requirements.txt /

RUN pip install spacy==2.0.18 \
  && python -m spacy download en_core_web_sm \
  && pip install -r requirements.txt

COPY . /app
WORKDIR /app

RUN pip install .

CMD trumptweets