web: gunicorn proj_bookmeteranalyzer.wsgi
worker: celery worker -A proj_bookmeteranalyzer.celery --pool=solo -l INFO