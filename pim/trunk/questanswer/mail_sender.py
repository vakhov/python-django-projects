# -*- coding: utf8 -*-
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import datetime

def send_mail(author, question, date=datetime.datetime.now()):
    context = {}
    context['author'] = author
    context['question'] = question
    context['date'] = date
    subject, from_email, to = 'На сайт pim66.ru поступил новый вопрос.', settings.MAIL_FROM, settings.MAIL_TO
    html_content = render_to_string('qa/send_form.html', context)
    msg = EmailMultiAlternatives(subject, '', from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()