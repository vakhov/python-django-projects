# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from utils.tree import build_tree
from utils.decorators import staff_required

from structure.models import Section, SectionType

from models import Position, QuestAnswer, Image, News, File, SpecialOffer, Feedback, Tag, FeedbackFlora, Pictures
from basket import Basket
from shortcuts import paginate

NEWS_ON_PAGE = 10
QA_ON_PAGE = 10
TOV_ON_PAGE = 12
TAG_ON_PAGE = 10

def index(request):
    context = RequestContext(request)
    context['title'] = u'Главная страница'
    context['news'] = News.objects.filter(section=Section.objects.get(path='/news/')).order_by('-date')[:3]
    context['tags'] = Tag.objects.all()
    # files...
    return render_to_response('flora/index.html', context)

def text(request):
    context = RequestContext(request)
    context['title'] = u'Главная страница'
    return render_to_response('flora/text.html', context)

def form(request):
#    return HttpResponse('Form page')
    
    context = RequestContext(request)
    context['title'] = u'Главная страница'
    c = {}
    c.update(csrf(request))
    
#    forms = {}
#    # kol = {}
#    all_price = 0
#    for key in request.session.keys():
#        if is_numeric(key):
#            tov = Position.objects.get(pk=key)
#            price = tov.price_rozn*request.session[key]
#            all_price += price
#            forms[key] = {'tov':Position.objects.get(pk=key).get_all,
#                          'kol':request.session[key],
#                          'price':price}
#        else:
#            continue
#    if len(forms) > 0:
#        context['forms'] = forms
#        context['all_price'] = all_price

    context['c'] = c
    context['title'] = u'Обратная связь'
    context['fio_error'] = False
    context['cont_error'] = False
    context['mes_error'] = False
    if request.method == 'POST':

        if not request.POST.get('r_autor', ''):
            context['fio_error'] = True
        else:
            context['r_autor'] = request.POST['r_autor']

        if not request.POST.get('r_cont', ''):
            context['cont_error'] = True
        else:
            context['r_cont'] = request.POST['r_cont']

        if not request.POST.get('r_mes', ''):
            context['mes_error'] = True
        else:
            context['r_mes'] = request.POST['r_mes']

        if context['fio_error'] or context['cont_error'] or context['mes_error']:
            return render_to_response('flora/form.html', context)
        else:
#            if context['forms']:
#                send_mail(u'Заказ', 
#                            u'Автор: ' + context['r_autor'] + 
#                            u'.\r\n Контактная информация: ' + context['r_cont'] +
#                            u'. Сообщение: ' + context['r_mes'] +
#                            u'Заказал ' + '' + u'шт. товара, на сумму ' + str(context['all_price']),
#                            'noreply@example.com',
#                            ['succubi@pixelion.ru',],
#                        )
#                reservation = Reservation(form=order['order'],sender = context['r_autor'], contact = context['r_cont'], message = context['r_mes'])
#                reservation.save()
#                return HttpResponseRedirect('/form/')
#            else:
#                send_mail(u'Заявка с сайта', 
#                            u'Автор: ' + context['r_autor'] + 
#                            u'.\r\n Контактная информация: ' + context['r_cont'] +
#                            u'. Сообщение: ' + context['r_mes'],
#                            'noreply@example.com',
#                            ['succubi@pixelion.ru',],
#                        )
                form = Feedback(sender=context['r_autor'], contact=context['r_cont'], message=context['r_mes'])
                form.save()
                return HttpResponseRedirect('/form/')
    else:
        return render_to_response('flora/form.html', context)
    

def catalog_list(request, page=None):
    context = RequestContext(request)
    context['title'] = u'Портфолио'
    paginate(
        context, 'catalog',
        Position.objects.filter(section=context['current_section']).order_by('order'),
        count=TOV_ON_PAGE, page=page,
        root=context['current_section'].path
    )

    basket = Basket(request.session)
    for position in context['catalog']:
        position.count_in_basket = basket.position_count(position.id)

    return render_to_response('flora/catalog.html', context)

def catalog_item(request, position_id):
    context = RequestContext(request)
    context['title'] = u'Портфолио'
    context['position'] = get_object_or_404(Position, pk=position_id)
    context['position_image'] = Position.get_image(position_id)[0]
    context['gallery'] = Pictures.get_image(position_id, 'Pictures')
    basket = Basket(request.session)
    context['position'].count_in_basket = basket.position_count(position_id)
    return render_to_response('flora/catalog-item.html', context)

@staff_required
def catalog_all(request):
    context = RequestContext(request)
    context['title'] = u'Портфолио'
    context['catalog_all'] = Position.objects.filter(section=context['current_section']).order_by('order')
    return render_to_response('flora/catalog-all.html', context)

@staff_required
def move_position(request, id, new_order):
    try:
        position = Position.objects.get(pk=id)
        position.move(new_order)
        position.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('BAD')

def tag(request, tag, page=None):
    context = RequestContext(request)
    context['title'] = u'Tag'
    context['tagview'] = get_object_or_404(Tag, name=tag)
    paginate(
        context, 'catalog', 
        query=Position.objects.filter(tags__name__exact=tag),
        count=TAG_ON_PAGE, page=page, 
        root=request.current_section.path+tag+'/'
    )
    return render_to_response('flora/tag.html', context)

########BASKET########

##------ADD------
#def add_to_basket(request, position_id):
#    context = RequestContext(request)
#    basket = Basket(request)
#    basket.add(position_id, 1)
#
#    if request.GET.get('redirect_to'):
#        return HttpResponseRedirect(request.GET['redirect_to'])
#    else:
#        import json
#        return HttpResponse(json.dumps(basket.session['basket']))
#
##------DELETE------
#def del_to_basket(request, item_catalog=None, redirect=None):
#    item_catalog = int(item_catalog)
#    context = RequestContext(request)
#    get_object_or_404(Position, pk=item_catalog)
#
#    if request.session.get(item_catalog, None):
#        if request.session[item_catalog] <= 1:
#            del request.session[item_catalog]
#            if redirect == 'form':
#                return HttpResponseRedirect('/form/')
#            else:
#                return HttpResponseRedirect('../')
#        else:
#            request.session[item_catalog] -= 1    
#    
#    if redirect == None:
#        return HttpResponseRedirect('../#add')
#    elif redirect == 'form':
#        return HttpResponseRedirect('/form/')
#    else:
#        return HttpResponseRedirect('/')
#
##------REMOVE------
#def rem_to_basket(request):
#    if request.session.get('basket', None):
#        del request.session['basket']
#        return HttpResponseRedirect('/form/')
#    else:
#        return HttpResponseRedirect('/form/')
#
#########END_BASKET########

def news(request, slug=None, item_news=None, page=None):
    context = RequestContext(request)
    context['title'] = u'Новости'
    if slug is None and item_news is None and news:
        paginate(
            context, 'news',
            News.objects.filter(section=context['current_section']).order_by('-date'),
            count=NEWS_ON_PAGE, page=page,
            root='/news/'
        )
        return render_to_response('flora/news.html', context)
    elif item_news is None and slug is not None:
        context['news'] = get_object_or_404(News, slug=slug)
        return render_to_response('flora/news-item.html', context)
    elif slug is None and item_news is not None:
        context['news'] = get_object_or_404(News, pk=item_news)
        return render_to_response('flora/news-item.html', context)

def article(request, slug=None, item_news=None, page=None):
    context = RequestContext(request)
    context['title'] = u'Статьи'
    if slug is None and item_news is None:
        paginate(
            context, 'news',
            News.objects.filter(section=context['current_section']).order_by('-date'),
            count=NEWS_ON_PAGE, page=page,
            root='/article/'
        )
        return render_to_response('flora/article.html', context)
    elif item_news is None and slug is not None:
        context['news'] = get_object_or_404(News, slug=slug)
        return render_to_response('flora/article-item.html', context)
    elif slug is None and item_news is not None:
        context['news'] = get_object_or_404(News, pk=item_news)
        return render_to_response('flora/article-item.html', context)

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
            qa = QuestAnswer(author=context['q_autor'], question=context['q_mes'])
            qa.save()
            context['ok'] = True

    paginate(
        context, 'questanswer',
        QuestAnswer.objects.order_by('-publication_date').filter(is_public=True),
        count=QA_ON_PAGE, page=page,
        root=context['current_section'].path
    )
    return render_to_response('flora/questanswer.html', context)

def feedbackflora(request, page=None):
    context = RequestContext(request)
    context['title'] = u'Отзыв'
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
            qa = FeedbackFlora(
                             author=context['q_autor'],
                             question=context['q_mes'],
                             work=request.POST.get('q_work', ''),
                             punkt=request.POST.get('q_punkt', ''),
                             
                             )
            qa.save()
            context['ok'] = True

    paginate(
        context, 'feedbackflora',
        FeedbackFlora.objects.order_by('-publication_date').filter(is_public=True),
        count=QA_ON_PAGE, page=page,
        root=context['current_section'].path
    )
    context['unanswered'] = FeedbackFlora.objects.order_by('-publication_date').filter(is_public=False)
    return render_to_response('flora/questanswer.html', context)
