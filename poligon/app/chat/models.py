# -*- coding: utf8 -*-

import hashlib
import datetime

from django.db import models
from django import forms

class User(models.Model):
	"""
	User
	"""
	STATUS_CHOICES = (
		('user', 'Пользователь'),
		('manager', 'Менеджер'),
	)

	login = models.CharField(u'Логин', max_length=20, unique=True)
	password = models.CharField(u'Пароль', max_length=32)
	email = models.EmailField(u'E-Mail', blank=True)
	status = models.CharField(u'Статус', max_length=7, choices=STATUS_CHOICES, blank=True)

	class Meta:
		verbose_name = u'Пользователь'
		verbose_name_plural = u'Пользователи'

	def __unicode__(self):
		return '%s' % self.login

	def save(self, *args, **kwargs):
		if not self.id:
			self.password = hashlib.md5(str(self.password)).hexdigest()
		else:
			try:
				user = User.objects.get(login=self.login)
				pwd = hashlib.md5(str(self.password)).hexdigest()
				if user.password != pwd:
					self.password = pwd
			except:
				pass
			
		if not self.status:
			self.status = u'user'
		super(User, self).save(*args, **kwargs)

class UserForm(forms.ModelForm):
	"""
	registration Form
	"""
	login = forms.CharField(label=u'Логин', widget=forms.TextInput(attrs={'size': '20', 'id': 'login'}), min_length=3, max_length=20)
	password = forms.CharField(label=u'Пароль', widget=forms.TextInput(attrs={'size': '20', 'id': 'pwd'}), min_length=4, max_length=20)

	class Meta:
		model = User

	def clean_login(self):
		login = self.cleaned_data['login']
		count = len(login)
		if not count:
			raise forms.ValidationErrors(u'Логин пуст')
		elif count < 3:
			raise forms.ValidationErrors(u'Логин менее 3 символов')
		elif count > 20:
			raise forms.ValidationErrors(u'Логин более 20 символов')
		return login

	def clean_password(self):
		pwd = self.cleaned_data['password']
		count = len(pwd)
		if not count:
			raise forms.ValidationErrors(u'Пароль пуст')
		elif count < 4:
			raise forms.ValidationErrors(u'Пароль менее 4 символов')
		elif count > 20:
			raise forms.ValidationErrors(u'Пароль более 20 символов')
		return pwd

class Chat(models.Model):
	"""
	Chat
	"""
	name = models.CharField(u'Имя', max_length=20)
	message = models.TextField(u'Сообщение')
	time = models.DateTimeField(u'Время', default=datetime.datetime.now())
	session = models.CharField(u'Сессия', max_length=32)

	class Meta:
		verbose_name = u'Чат'
		verbose_name_plural = u'Чаты'

	def __unicode__(self):
		return '(%s) - %s' % (self.name, self.message)
