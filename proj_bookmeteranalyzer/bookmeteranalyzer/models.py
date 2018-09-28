from django.db import models


class Post(models.Model):
    # Postメッセージ時のユーザID
    user_id = models.CharField(max_length=20)


class AnalyzeResult(models.Model):
    # ユーザIDを主キーとし，画像ファイルパスを保持する
    user_id = models.CharField(primary_key=True, max_length=20)
    img_file = models.ImageField(upload_to='image/')
    csv_file = models.FileField(upload_to='csv/')


