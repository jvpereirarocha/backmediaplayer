#!/bin/bash

ROOTDIR=$(pwd)

export $(grep -v '^#' .env | xargs)

DB_URI="${DATABASE_DRIVER}://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DATABASE_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

export DATABASE_URI=$DB_URI

cd db/migrations && alembic upgrade head && cd $ROOTDIR && gunicorn --bind=0.0.0.0:${SERVER_PORT} --workers=2 "main:create_app('${FLASK_ENV}')"