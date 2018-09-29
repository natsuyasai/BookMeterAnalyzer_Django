"""
WSGI config for proj_bookmeteranalyzer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj_bookmeteranalyzer.settings')

application = get_wsgi_application()


# スリープ対策
# import threading
# import requests
# import time

# def awake():
#     while True:
#         try:
#             print("Start Awaking")
#             requests.get("http://hogefuga.herokuapp.com/")
#             print("End")
#         except:
#             print("error")
#         time.sleep(300)

# t = threading.Thread(target=awake)
# t.start()