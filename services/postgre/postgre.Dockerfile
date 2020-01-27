FROM postgres:11.4-alpine

ADD ./config/db.sql /docker-entrypoint-initdb.d
