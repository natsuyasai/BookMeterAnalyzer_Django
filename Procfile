web: gunicorn proj_bookmeteranalyzer.wsgi:application -b 0.0.0.0:$PORT
worker: celery worker -A proj_bookmeteranalyzer.celery --pool=solo -l INFO