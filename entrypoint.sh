#!/bin/bash

alembic upgrade head
&& gunicorn --bind=0.0.0.0:${SERVER_PORT} --workers=2 "main:create_app('${FLASK_ENV}')"