FROM python:3.8-alpine
# uWSGI dependencies needed
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
# Psycogp2 dependencies needed
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install psycopg2
# Pillow dependencies needed
RUN apk --update add \
    build-base \
    jpeg-dev \
    zlib-dev

ENV PATH="/scripts:${PATH}"

WORKDIR /twitter-clone

COPY ./twitter-clone-drf/requirements.txt ./

RUN pip install -r requirements.txt

RUN apk del .tmp

COPY ./twitter-clone-drf ./

COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media

RUN mkdir -p /vol/web/static

RUN adduser -D user

RUN chmod -R 755 ./

RUN chmod -R 755 /vol/web

USER user

CMD ["entrypoint.sh"]