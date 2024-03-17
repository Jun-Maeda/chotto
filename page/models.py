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
        verbose_name_plural = "3.サービス内容"

    name = models.ForeignKey(
        ServiceName,
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
    priority = models.FloatField(
        verbose_name='表示優先順位'
    )

    def __str__(self):
        return "[" + self.name.name + "]" + self.service_date.name + " " + self.service_time.name


class RoomType(models.Model):
    class Meta:
        verbose_name_plural = "3.部屋タイプ"

    name = models.CharField(
        max_length=50,
        verbose_name='部屋タイプ'
    )

    def __str__(self):
        return self.name


class ServicePrice(models.Model):
    class Meta:
        verbose_name_plural = "3.サービス料金設定"

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


# 部屋画像
class RoomImage(models.Model):
    img = models.ImageField(
        verbose_name='画像',
        blank=True, null=True,
    )

    def __str__(self):
        return self.img.name


class Room(models.Model):
    class Meta:
        verbose_name_plural = "2.部屋"

    name = models.CharField(
        max_length=50,
        verbose_name='部屋名',
    )
    type = models.ForeignKey(
        RoomType,
        verbose_name='タイプ',
        on_delete=models.CASCADE,
    )
    img = models.ManyToManyField(
        RoomImage,
        verbose_name='部屋画像',
        related_name='img_room',
        blank=True, null=True,
    )

    def __str__(self):
        return self.name


# 設備
class Facility(models.Model):
    class Meta:
        verbose_name_plural = "2.設備"

    name = models.CharField(
        max_length=50,
        verbose_name='設備'
    )
    img = models.ImageField(
        verbose_name='画像',
        blank=True, null=True,
    )
    vip_flg = models.BooleanField(
        verbose_name='VIP限定',
        default=False,
    )
    limited_room = models.ManyToManyField(
        Room,
        verbose_name='部屋限定',
        related_name='facility_room',
        null=True, blank=True
    )

    def __str__(self):
        return self.name


# メニュー関連
class MenuType(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='メニュージャンル'
    )
    priority = models.FloatField(
        verbose_name='表示優先順位'
    )

    def __str__(self):
        return self.name


class MenuCategory(models.Model):
    class Meta:
        verbose_name_plural = "2.メニューカテゴリー"

    name = models.CharField(
        max_length=50,
        verbose_name='メニューカテゴリー'
    )
    type = models.ForeignKey(
        MenuType,
        verbose_name='ジャンル',
        on_delete=models.CASCADE,
    )
    priority = models.FloatField(
        verbose_name='表示優先順位'
    )

    def __str__(self):
        return self.name


class Menu(models.Model):
    class Meta:
        verbose_name_plural = "1.メニュー"

    name = models.CharField(
        max_length=50,
        verbose_name='メニュー名',
    )
    category = models.ForeignKey(
        MenuCategory,
        verbose_name='カテゴリー',
        on_delete=models.CASCADE,
    )
    price = models.IntegerField(
        verbose_name='通常価格'
    )
    member_price = models.IntegerField(
        verbose_name='メンバー価格'
    )
    priority = models.FloatField(
        verbose_name='表示優先順位'
    )
    welcome_flg = models.BooleanField(
        default=False,
        verbose_name='ウェルカムフラグ'
    )
    text = models.TextField(
        verbose_name='詳細',
        null=True, blank=True,
    )


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
