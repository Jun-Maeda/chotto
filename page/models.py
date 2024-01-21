from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# 画像関連


# お知らせ
class Info(models.Model):
    class Meta:
        verbose_name_plural = "1.お知らせ&イベント"

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
        verbose_name='お知らせ',
        related_name='info_image',
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.img.name


# サービス関連
class ServiceDate(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='利用日'
    )
    priority = models.FloatField(
        verbose_name='表示優先順位'
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
        verbose_name='終日フラグ'
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

class ServiceName(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='サービス名'
    )
    priority = models.FloatField(
        verbose_name='表示優先順位'
    )
    def __str__(self):
        return self.name

# サービスの利用日と時間
class Service(models.Model):
    class Meta:
        verbose_name_plural = "1.サービス内容"
    name = models.ForeignKey(
        ServiceName,
        verbose_name='サービス名',
        on_delete=models.CASCADE,
    )
    servie_date = models.ForeignKey(
        ServiceDate,
        verbose_name='サービス利用日',
        on_delete=models.CASCADE,
    )
    service_time = models.ForeignKey(
        ServiceTime,
        verbose_name='サービス利用時間',
        on_delete=models.CASCADE,
    )
    priority = models.FloatField(
        verbose_name='表示優先順位'
    )

    def __str__(self):
        return "["+self.name.name + "]" + self.servie_date.name + " " + self.service_time.name


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
        verbose_name_plural = "1.サービス料金設定"

    room_type = models.ForeignKey(
        RoomType,
        verbose_name='部屋タイプ',
        on_delete=models.CASCADE,
    )
    service = models.ForeignKey(
        ServiceName,
        verbose_name='サービス名',
        on_delete=models.CASCADE,
    )
    service_date = models.ForeignKey(
        ServiceDate,
        verbose_name='サービス利用日',
        on_delete=models.CASCADE,
    )
    price = models.IntegerField(
        verbose_name='価格'
    )
    priority = models.FloatField(
        verbose_name='表示優先順位'
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

# メニュー関連
class MenuType(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='メニュージャンル'
    )
    def __str__(self):
        return self.name


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
    class Meta:
        verbose_name_plural = "1.メニュー"


class MenuImage(models.Model):
    img = models.ImageField(
        verbose_name='画像',
        blank=True, null=True,
    )
    menu = models.ForeignKey(
        Menu,
        verbose_name='メニュー',
        related_name='menu_image',
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.img.name
