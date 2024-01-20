from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# 画像関連


# お知らせ
class Info(models.Model):
    class Meta:
        verbose_name_plural = "お知らせ&イベント"
    user = models.ForeignKey(
        User,
        verbose_name='作成ユーザー名',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=50,
        verbose_name='タイトル',
    )
    detail = models.TextField(
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
    event_flg = models.BooleanField(
        default=False,
        verbose_name='イベントフラグ'
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


# サービス関連
class ServiceDate(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='利用日'
    )

    def __str__(self):
        return self.name


class ServiceTime(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='利用時間'
    )
    all_flg = models.BooleanField(
        default=False,
        verbose_name='全日フラグ'
    )
    start_time = models.TimeField(
        verbose_name='開始時間',
        blank=True, null=True,
    )
    end_time = models.TimeField(
        verbose_name='終了時間',
        blank=True, null=True,
    )
    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='サービス名'
    )
    def __str__(self):
        return self.name


# Todo:部屋のタイプで料金が変わるのか確認
class RoomType(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='部屋タイプ'
    )
    def __str__(self):
        return self.name


class ServicePrice(models.Model):
    class Meta:
        verbose_name_plural = "サービス料金設定"
    room_type = models.ForeignKey(
        RoomType,
        verbose_name='部屋タイプ',
        on_delete=models.CASCADE,
    )
    service = models.ForeignKey(
        Service,
        verbose_name='サービス名',
        on_delete=models.CASCADE,
    )
    service_date = models.ForeignKey(
        ServiceDate,
        verbose_name='サービス利用日',
        on_delete=models.CASCADE,
    )
    service_time = models.ForeignKey(
        ServiceTime,
        verbose_name='サービス利用時間',
        on_delete=models.CASCADE,
    )
    price = models.IntegerField(
        verbose_name='価格'
    )


class Facility(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='設備'
    )


class Room(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='部屋名',
    )
    type = models.ForeignKey(
        RoomType,
        verbose_name='タイプ',
        on_delete=models.CASCADE,
    )


class MenuType(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='メニュージャンル'
    )


class Menu(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='メニュー名',
    )
    type = models.ForeignKey(
        MenuType,
        verbose_name='ジャンル',
        on_delete=models.CASCADE,
    )
    price = models.IntegerField(
        verbose_name='価格'
    )
