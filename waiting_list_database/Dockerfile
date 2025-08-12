FROM postgres:alpine

ENV POSTGRES_USER=waitinglist
ENV POSTGRES_PASSWORD=secret
ENV POSTGRES_DB=waitinglist

COPY ./src/ /docker-entrypoint-initdb.d/
