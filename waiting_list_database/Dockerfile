FROM postgres:alpine

ENV POSTGRES_USER=billy
ENV POSTGRES_PASSWORD=secret
ENV POSTGRES_DB=billy

COPY ./src/ /docker-entrypoint-initdb.d/