from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# 画像関連


# お知らせ
class Info(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='作成ユーザー名',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=50,
        verbose_name='タイトル',
    )
    detail = models.CharField(
        max_length=500,
        verbose_name='本文',
    )
    make_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='作成日'
    )
    update_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='更新日'
    )

# お知らせ画像
class InfoImage(models.Model):
    img = models.ImageField(
        verbose_name='画像',
        blank=True, null=True,
    )
    info = models.ForeignKey(
        Info,
        verbose_name='画像',
        related_name='image',
        on_delete=models.CASCADE,
        blank=True, null=True,
    )