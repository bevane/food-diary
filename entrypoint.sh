#!/usr/bin/env bash
uv run manage.py collectstatic --noinput
uv run manage.py migrate --noinput
uv run gunicorn -b :8000 food_diary.wsgi
