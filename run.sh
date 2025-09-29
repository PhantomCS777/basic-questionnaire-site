#!/bin/bash
export FLASK_APP=app.py
# python3 -m flask run --host=0.0.0.0 --port=5050
gunicorn --workers 4 --worker-class gevent --bind 0.0.0.0:5050 app:app