# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from utils.shortcuts import paginate
from structure.models import Section, SectionType
from django.core.context_processors import csrf
from django.conf import settings

# импорт моделей
from questanswer.models import QuestAnswer, TagName, Alphabet

QA_ON_PAGE = 10

def questanswer(request, page=None):
    context = RequestContext(request)
    context['title'] = u'Вопрос-ответ'
    if request.method == 'POST':
        context['author_error'] = False
        context['mes_error'] = False

        if not request.POST.get('q_autor', ''):
            context['author_error'] = True
        else:
            context['q_autor'] = request.POST['q_autor']
        
        if not request.POST.get('q_mes', ''):
            context['mes_error'] = True
        else:
            context['q_mes'] = request.POST['q_mes']
        
        if context['author_error'] or context['mes_error']:
            pass
        else:
            qa = QuestAnswer(author = context['q_autor'], question = context['q_mes'])
            qa.save()
            context['ok'] = True
    context['unanswered'] = QuestAnswer.objects.order_by('-date_publication').filter(is_public=False)
    context['tags'] = TagName.objects.all()
    context['alphabet'] = Alphabet.objects.filter(is_action=True).order_by('letter')
    paginate(
        context, 'questanswer', 
        QuestAnswer.objects.order_by('-date_publication').filter(is_public=True),
        count=QA_ON_PAGE, page=page, 
        root=context['current_section'].path
    )
    return render_to_response('qa/questanswer.html', context)

def question(request, id):
    context = RequestContext(request)
    context['title'] = u'Вопрос-ответ'
    context['question'] = QuestAnswer.objects.get(id=id)
    return render_to_response('qa/question.html', context)

def tag(request, slug):
    tag = TagName.objects.get(slug=slug)
    context = RequestContext(request)
    context['title'] = u'Вопрос-ответ'
    context['tag'] = tag
    context['unanswered'] = tag.questanswer_set.all()
    return render_to_response('qa/questanswer.html', context)
