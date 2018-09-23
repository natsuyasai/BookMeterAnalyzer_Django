from django.db import models


class Post(models.Model):
    # Postメッセージ時のユーザID
    userID = models.CharField(max_length=200)