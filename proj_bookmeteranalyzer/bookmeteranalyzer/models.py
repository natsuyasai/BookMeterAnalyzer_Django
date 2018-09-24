from django.db import models


class Post(models.Model):
    # Postメッセージ時のユーザID
    user_id = models.CharField(max_length=20)


class AnalyzeResult(models.Model):
    img_file = models.ImageField(upload_to='image')
