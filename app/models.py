from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from accounts.models import CustomUser
import os
from django.urls import reverse


class MyList(models.Model):
    """マイリスト"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    created = models.DateTimeField("作成日", default=timezone.now)
    
    class Meta:
        verbose_name = "マイリスト一覧"
        verbose_name_plural = "マイリスト一覧"

    def __str__(self):
        return f"{self.user.first_name} {self.movie_id} {self.created}"
    

class Review(models.Model):
    """レビュー"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie_id = models.IntegerField("アイテムID", blank=False, null=False) #max_length=255, 
    title = models.CharField("タイトル", max_length=30)
    content = models.TextField("本文", blank=False, null=False, max_length=320000)
    like = models.IntegerField("評価", validators=[MinValueValidator(1), MaxValueValidator(5)], default=3)
    spoiler = models.BooleanField("ネタバレ", default=False)
    publish = models.BooleanField("公開", default=True)
    updated = models.DateTimeField("更新日", default=timezone.now)
    created = models.DateTimeField("作成日", default=timezone.now)

    def __str__(self):
        return f'タイトル: {self.title} | 評価:{self.like} | 投稿者: {self.author.user_screen_id}'
    
    def get_avatar_url(self):
        return self.author.avatar
    
    class Meta:
        verbose_name = "レビュー一覧"
        verbose_name_plural = "レビュー一覧"

class KeyWords(models.Model):
    """KeyWords"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    keywords = models.TextField("キーワード", blank=False, null=False, max_length=455)
    created = models.DateTimeField("作成日", default=timezone.now)
    
    class Meta:
        verbose_name = "キーワード"
        verbose_name_plural = "キーワード"

    def __str__(self):
        return f"担当者: {self.user.first_name} {self.user.last_name} | 日付: {self.created}"
    

class Description(models.Model):
    """Description"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField("詳細", blank=False, null=False, max_length=120)
    created = models.DateTimeField("作成日", default=timezone.now)
    
    class Meta:
        verbose_name = "サイト詳細"
        verbose_name_plural = "サイト詳細"

    def __str__(self):
        return f"担当者: {self.user.first_name} {self.user.last_name} | 日付: {self.created}"