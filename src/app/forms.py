from django import forms

from django.db import models

class PostReview(forms.Form):
    title = forms.CharField(label='タイトル', max_length=30)
    content = forms.CharField(label='本文', widget=forms.Textarea(), max_length=320000)
    spoiler = forms.BooleanField(label='ネタバレ', required=False, widget=forms.CheckboxInput())
    publish = forms.BooleanField(label='公開', required=False, widget=forms.CheckboxInput())
    # like = forms.IntegerField(label='評価', min_value=1, max_value=5)

class Search(forms.Form):
    words = forms.CharField(label='検索ワード', max_length=255)
