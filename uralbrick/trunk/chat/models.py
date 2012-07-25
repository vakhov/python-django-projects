# -*- coding: utf8 -*-

import datetime

from django.db import models
from django import forms

class Chat(models.Model):
    """
    Chat
    """
    name = models.CharField('Имя', max_length=20)
    message = models.TextField('Сообщение')
    time = models.DateTimeField('Время', default=datetime.datetime.now())
    session = models.CharField('Сессия', max_length=32)
    status = models.BooleanField('Закрыто', default=False, blank=True)
    
    
    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(Chat, self).save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        super(Chat, self).delete(*args, **kwargs)

class ChatForm(forms.ModelForm):
    """
    ChatForm
    """
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'cols':'20','rows':'2'}))
    
    class Meta:
        model = Chat

class LoginForm(forms.ModelForm):
    """
    LoginForm
    """
    login = forms.CharField(label='Ваше имя?', widget=forms.TextInput(attrs={'size':'20', 'id':'login'}))
    
    class Meta:
        model = Chat
    