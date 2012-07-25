# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django import forms
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class Order(models.Model):
    name = models.CharField(u'ФИО покупателя', max_length=255)
    email = models.EmailField(u'e-mail покупателя', blank=True)
    phone = models.CharField(u'Телефон покупателя', max_length=50)
    #address block
    index = models.CharField(u'Индекс', max_length=6, blank=True)
    city = models.CharField(u'Город', max_length=255, blank=True)
    street = models.CharField(u'Улица', max_length=100, blank=True)
    house = models.CharField(u'Дом', max_length=10, blank=True)
    apartment = models.CharField(u'Квартира', max_length=30, blank=True)
    #address block
    comment = models.TextField(u'Комментарий', blank=True)
    order_human_form = models.TextField(u'Заказ (человеческий вид)', blank=True)
    order_native_form = models.TextField(u'Заказ (машинный вид)', blank=True)
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        return self.id
    
    
    def send_mail(self, form, basket, basket_info, session):
        context = {}
        #Наполняем контекст значениями из формы для рендинга в шаблоне ответа
        context['name']        = form['name']
        context['email']       = form['email']
        context['phone']       = form['phone']
        context['index']       = form['index']
        context['city']        = form['city']
        context['street']      = form['street']
        context['house']       = form['house']
        context['apartment']   = form['apartment']
        context['comment']     = form['comment']
        
        #Добавляем информацию о товарах из корзины и о текущей сумме заказа
        context['basket'] = basket
        context['basket_info'] = basket_info
        
        #Сохраняем заказ в базе и получаем ID текущего заказа. Помещаем ID так же в контекст
        order = Order(
                      name = form['name'],
                      email = form['email'],
                      phone = form['phone'],
                      index= form['index'],
                      city = form['city'],
                      street = form['street'],
                      house  = form['house'],
                      apartment = form['apartment'],
                      comment = form['comment'],
                      order_human_form = render_to_string('basket/send_form.html', context),
                      order_native_form = session['basket']
                      )
        num_order = order.save()
        context['num_order'] = num_order
        
        #Формируем всё что необходимо для отправки письма, рендерим форму и отправляем письмо.
        subject, from_email, to = 'Заказ №' + str(num_order) + ' с сайта pim66.ru', settings.MAIL_FROM, settings.MAIL_TO
        html_content = render_to_string('basket/send_form.html', context)
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
    
    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'

class OrderForm(forms.ModelForm):
    name = forms.CharField(label=u'ФИО:', widget=forms.TextInput(attrs={'size':'44'}))
    email = forms.EmailField(label=u'E-mail:', widget=forms.TextInput(attrs={'size':'33'}), required=False)
    phone = forms.CharField(label=u'Телефон:', widget=forms.TextInput(attrs={'value':'+7'}))
    index = forms.CharField(label=u'Индекс', widget=forms.TextInput(attrs={'size':'11'}), required=False)
    house = forms.CharField(label=u'Дом', widget=forms.TextInput(attrs={'size':'11'}), required=False)
    apartment = forms.CharField(label=u'Квартира', widget=forms.TextInput(attrs={'size':'11'}), required=False)
    comment = forms.CharField(label=u'Комментарий', required=False, widget=forms.Textarea)
    
    class Meta:
        model = Order
