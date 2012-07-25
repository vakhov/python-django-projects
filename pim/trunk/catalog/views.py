# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from utils.shortcuts import paginate
from models import Product, Section, Catalog, Pricing, NewCollection
from models import BooleanPropertyValue, CharPropertyValue, NumericPropertyValue, MultipleChoicePropertyValue, Property, Choice, Action
from order import Order, OrderForm
from title.models import Title, ChangeTitle
from seo.models import Metatag
from utils.decorators import staff_required
from utils.tree import build_tree
from structure.models import SectionType
from questanswer.models import QuestAnswer

#from questanswer.mail_sender import send_mail

from basket import Basket

import json

PRODUCTS_ON_PAGE = 32
COLLECTIONS_ON_PAGE = 10

def get_default_context(request):
    """
    Gets default context variables for catalog:
    - Subtree of catalog section
    - "New collections"
    """
    context = RequestContext(request)
    catalog_order = Section.objects.values('order').get(path='/catalog/')['order']
    context['catalog_tree'] = context['structure'][1]['nodes'][catalog_order]['nodes']
    return context    

def get_extended_properties(product):
    # Calculating "extended" properties
    props = product.catalog.properties.all()
    
    # Filling properties with their values
    charpvs = CharPropertyValue.objects.filter(position=product)
    numpvs = NumericPropertyValue.objects.filter(position=product)
    boolpvs = BooleanPropertyValue.objects.filter(position=product)
    mulpvs = MultipleChoicePropertyValue.objects.filter(position=product)
    
    properties = {}
    for p in props:
        if p.type == 4:
            properties[p.name] = {'val': p.choice_set.get(is_default=True).value, 'val_desc': p.choice_set.get(is_default=True).description, 'obj': p.description}
        elif p.type == 3:
            properties[p.name] = {'val': p.default and "Да" or "Нет", 'val_desc': p.description, 'obj': p.description}
        else:
            properties[p.name] = {'val' :p.default, 'val_desc': p.description, 'obj': p.description}
    for p in charpvs:
        properties[p.property.name] = {'val': p.value, 'val_desc': p.value.description, 'obj': p.property.description}
    for p in numpvs:
        properties[p.property.name] = {'val': p.value, 'val_desc': p.value.description, 'obj': p.property.description}
    for p in boolpvs:
        properties[p.property.name] = {'val': p.value and "Да" or "Нет", 'val_desc': p.value.description, 'obj': p.property.description}    
    for p in mulpvs:
        properties[p.property.name] = {'val': p.value.value, 'val_desc': p.value.description, 'obj': p.property.description}
    
    return properties

# Index page
def index(request):
    context = get_default_context(request)
    context['catalog_positions'] = Product.objects.filter(is_exist=True, 
                                                          on_main=True, 
                                                          is_enabled=True
                                                         ).order_by('?')[:8]
    return render_to_response('catalog/index.html', context)

# Catalog list (any sub-section)
def catalog_list(request, page=None):
    context = get_default_context(request)
    # Getting catalog for the section
    # @todo improve! o___O
    cs = context['current_section']
    if cs.path != '/catalog/':
        if Catalog.objects.filter(section=cs):
            context['catalog'] = Catalog.objects.get(section=cs)
        elif Catalog.objects.filter(section=cs.parent):
            context['catalog'] = Catalog.objects.get(section=cs.parent)
        elif Catalog.objects.filter(section=cs.parent.parent):
            context['catalog'] = Catalog.objects.get(section=cs.parent.parent)
        else:
            context['catalog'] = Catalog.objects.get(section=cs.parent.parent.parent)
        context['catalog_properties'] = context['catalog'].properties.all()
    else:
        context['catalog'] = None
        context['catalog_properties'] = []
        
    for p in context['catalog_properties']:
        if p.type == 4:
            fv = request.GET.getlist(p.slug)
            if fv is not None:
                arr = []
                for v in fv:
                    arr.append(int(v))
                p.filtered_values = arr
        else:
            fv = request.GET.get(p.slug)
            if fv is not None:
                p.filtered_value = fv
    
    # Is it terminal section or not?
    if context['current_section'].has_children():
        # Non-terminal section
        context['subsections'] = context['current_section'].children.filter(is_enabled=True)
        current_path = context['current_section'].path
        descendants_ids = Section.objects.filter(path__startswith=current_path).values('id')
        descendants_ids = [x['id'] for x in descendants_ids]
        if context['aphaline_edit_mode']:
            paginate(
                context, 'catalog_positions', 
                Product.objects.filter(section__in=descendants_ids) \
                                .filter(is_exist=True).order_by('-is_enabled', '-order'),
                count=PRODUCTS_ON_PAGE, page=page, 
                root=context['current_section'].path
            )
        else:
            paginate(
                context, 'catalog_positions', 
                Product.objects.filter(section__in=descendants_ids) \
                                .filter(is_exist=True, is_enabled=True).order_by('-order'),
                count=PRODUCTS_ON_PAGE, page=page, 
                root=context['current_section'].path
            )
        return render_to_response('catalog/list_nonterminal.html', context)
    else:
        if context['aphaline_edit_mode']:
            paginate(
                context, 'catalog_positions', 
                Product.objects.filter(section=context['current_section']).order_by('-is_enabled', '-is_exist', '-order'),
                count=PRODUCTS_ON_PAGE, page=page, 
                root=context['current_section'].path
            )
        else:
            paginate(
                context, 'catalog_positions', 
                Product.objects.filter(section=context['current_section'], is_enabled=True).order_by('-is_exist', '-order'),
                count=PRODUCTS_ON_PAGE, page=page, 
                root=context['current_section'].path
            )
        return render_to_response('catalog/list_terminal.html', context)

# Catalog item
def catalog_item(request, slug):
    context = get_default_context(request)
    product = get_object_or_404(Product, slug=slug)
    context['catalog'] = product.catalog
    context['catalog_properties'] = context['catalog'].properties.all()
    
    for size in product.pricing_set.all():
        if size.is_exist:
            context['size_is_exist'] = size.size_id
            break
    
    for p in context['catalog_properties']:
        if p.type == 4:
            fv = request.GET.getlist(p.slug)
            if fv is not None:
                p.filtered_values = fv
        else:
            fv = request.GET.get(p.slug)
            if fv is not None:
                p.filtered_value = fv

    context['catalog_position'] = product
    context['catalog_position_wtp'] = product.wtp.all()
    context['catalog_position_pricing'] = Pricing.objects.filter(product=product).order_by('size')
    context['catalog_position_images'] = product.picture_set.all()
    context['properties'] = get_extended_properties(product)
    context['crumbs'].append({ 
      'caption': product.name, 
      'path': context['current_section'].path + product.slug + '/'
    })
    basket = Basket(request.session)
    context['order_count'] = basket.get_count(product.id)
    
    #title
    if not Metatag.objects.filter(name=context['current_section'].path + product.slug + '/') \
        and product.catalog_id == 10: #пока что только для каталога Обувь
        if not ChangeTitle.objects.filter(path=context['current_section'].path + product.slug + '/'):            
            word_1 = Title.objects.filter(position=1).order_by('?')[0].title
            while True:
                word_2 = Title.objects.filter(position=2).order_by('?')[0].title
                if word_2.lower() != word_1.lower():
                    break
            while True:
                word_3 = Title.objects.filter(position=3).order_by('?')[0].title
                if word_3.lower() != word_1.lower() and word_3.lower() != word_2.lower():
                    break
            while True:
                word_4 = Title.objects.filter(position=4).order_by('?')[0].title
                if word_4.lower() != word_1.lower() and word_4.lower() != word_2.lower() and word_4.lower() != word_3.lower():
                    break
            title = ChangeTitle(path=context['current_section'].path + product.slug + '/', title='%s %s %s %s %s' % (word_1, word_2, context['catalog_position'].name, word_3, word_4))
            title.save()
            context['catalog_position'].title = '%s %s %s %s %s' % (word_1, word_2, context['catalog_position'].name, word_3, word_4)
        else:
            context['catalog_position'].title = ChangeTitle.objects.filter(path=context['current_section'].path + product.slug + '/')[0].title
    #title
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
#            send_mail(context['q_autor'], context['q_mes'])
            qa.save()
            qa.product_set.add(product)
            context['ok'] = True
    context['unanswered'] = product.qa.order_by('-date_publication').filter(is_public=False)
    context['questanswer'] = product.qa.order_by('-date_publication').filter(is_public=True)
    if 'ajax' in request.GET:
        return render_to_response('catalog/position_ajax.html', context)
    else:
        return render_to_response('catalog/position.html', context)

@staff_required
def catalog_all(request):
    context = get_default_context(request)
    context['catalog_all'] = Product.objects.filter(section=context['current_section']).order_by('-order')
    return render_to_response('catalog/catalog_all.html', context)

@staff_required
def move_position(request, id, new_order):
    try:
        product = Product.objects.get(pk=id)
        product.move(new_order)
        product.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('BAD')

@staff_required
def catalog_shuffle(request):
    import random
    context = get_default_context(request)
    catalog = Product.objects.filter(section=context['current_section'])
    count = range(1, len(catalog)+1)
    for position in catalog:
        current_random = count.pop((random.randint(1, len(count)))-1)
        position.move(current_random)
        position.save()
    return HttpResponseRedirect('../')
    

def collections_list(request, page=None):
    context = get_default_context(request)
    context['collections'] = NewCollection.objects.filter(is_active=True)
    paginate(
        context, 'collections', 
        NewCollection.objects.filter(is_active=True).order_by('-id'),
        count=COLLECTIONS_ON_PAGE, page=page, 
        root=context['current_section'].path
    )
    context['disables'] = NewCollection.objects.filter(is_active=False).order_by('-id')
    return render_to_response('collections/collections.html', context)

def collections_item(request, slug, page=None):
    context = get_default_context(request)
    context['collection'] = get_object_or_404(NewCollection, slug=slug)
    context['crumbs'].append({
      'caption': context['collection'].name,
      'path': slug,
    })
    paginate(
        context, 'positions', 
        query=NewCollection.objects.get(slug=slug).products.all().filter(is_enabled=True),
        count=PRODUCTS_ON_PAGE, page=page, 
        root=context['current_section'].path+slug+'/'
    )
    return render_to_response('collections/collections-item.html', context)

def basket_list(request):
    context = get_default_context(request)
    basket = Basket(request.session)
    basket_items = basket.get_list()
    
    if request.method == 'GET':
        # Showing basket to user
        context['basket'] = basket_items
        context['form'] = OrderForm()
    else:
        # Checking and posting the order
        form = OrderForm(request.POST)
        if form.is_valid():
            # Valid order
            # Saving to the model
            
            order = Order()
            form_cd  = form.cleaned_data
            summary_info = basket.get_summary_info()
            context['fields'] = order.send_mail(form_cd, basket_items, summary_info, request.session)
            basket.clear()
            return render_to_response('basket/good.html', context)
        else:
            # Invalid order: repeating form
            context['basket'] = basket_items
            context['form'] = form

    return render_to_response('basket/index.html', context)

@staff_required
def wtp(request, pk):
    context = get_default_context(request)
#    type = SectionType.objects.get(slug='catalog')
    nodes = Section.objects.filter(is_enabled=True).values()
    context['structure'] = build_tree(nodes)
    context['pk'] = pk
    return render_to_response('wtp/index.html', context)

@staff_required
def wtp_catalog(request, pid):
    context = get_default_context(request)
    product = Product.objects.get(pk=pid)
    wtp_pid = []
    for wtp in product.wtp.all():
        wtp_pid.append(wtp.id)
    context['wtp_pid'] = wtp_pid
    context['catalog'] = Product.objects.filter(section=Section.get_node_by_path(request.POST['current_section'])).order_by('-order')
    return render_to_response('wtp/catalog.html', context)
    #return HttpResponse(request.POST['current_section'])

@staff_required
def wtp_add(request, pid, wtp_pid):
    context = get_default_context(request)
    product = Product.objects.get(pk=pid)
    wtp_product = Product.objects.get(pk=wtp_pid)
    product.wtp.add(wtp_product)
    return HttpResponse('Product #%s add in %s' % (wtp_pid, pid))

@staff_required
def wtp_del(request, pid, wtp_pid):
    context = get_default_context(request)
    product = Product.objects.get(pk=pid)
    wtp_product = Product.objects.get(pk=wtp_pid)
    product.wtp.remove(wtp_product)
    return HttpResponse('Product #%s delete %s' % (wtp_pid, pid))

@staff_required
def collection_index(request, id):
    context = get_default_context(request)
    nodes = Section.objects.filter(is_enabled=True).values()
    context['structure'] = build_tree(nodes)
    context['collection_id'] = id
    return render_to_response('change_collection/index.html', context)

@staff_required
def collection_catalog(request, id):
    context = get_default_context(request)
    product_in_collecion = NewCollection.objects.get(pk=id)
    collecion_id = []
    for product in product_in_collecion.products.all():
        collecion_id.append(product.id)
    context['collecion_id'] = collecion_id
    context['catalog'] = Product.objects.filter(section=Section.get_node_by_path(request.POST['current_section'])).order_by('-order')
    return render_to_response('change_collection/catalog.html', context)

@staff_required
def collection_add(request, id, add_id):
    context = get_default_context(request)
    collection = NewCollection.objects.get(pk=id)
    product = Product.objects.get(pk=add_id)
    collection.products.add(product)
    return HttpResponse('Product #%s add in %s collection' % (add_id, id))

@staff_required
def collection_del(request, id, del_id):
    context = get_default_context(request)
    collection = NewCollection.objects.get(pk=id)
    product = Product.objects.get(pk=del_id)
    collection.products.remove(product)
    return HttpResponse('Product #%s delete %s collection' % (del_id, id))

def filter(request):
    context = get_default_context(request)
    catalog = request.POST['catalog']
    price_max = request.POST['price_max']
    price_min = request.POST['price_min']
    size = json.loads(request.POST['size'])
    context['product'] = Product.filter(str(catalog), int(price_min), int(price_max), size).values()
    return render_to_response('catalog/product.html', context)

@staff_required
def change_property(request):
    context = get_default_context(request)
    try:
        product = Product.objects.get(pk=request.POST['position'])
        mulcpv = MultipleChoicePropertyValue.objects.filter(position=product)
        property = Property.objects.get(pk=request.POST['property'])
        mulcpv = mulcpv.get(property=property)
        choise = Choice.objects.get(pk=request.POST['choise'])
        mulcpv.value = choise
        mulcpv.save()
    except:
        product = Product.objects.get(pk=request.POST['position'])
        property = Property.objects.get(pk=request.POST['property'])
        choise = Choice.objects.get(pk=request.POST['choise'])
        mulcpv = MultipleChoicePropertyValue(property=property, value=choise)
        product.multiplechoicepropertyvalue_set.add(mulcpv)
        product.save()
    return HttpResponse(request.POST['choise'] + '||' +request.POST['property'] + '||' +request.POST['position'] + '||')

def glossarium(request):
    context = get_default_context(request)
    propertys = Property.objects.all().order_by('name')
    choices = Choice.objects.filter(property__in=propertys).order_by('value')
    
    result = {}
    for property in propertys:
        if property.description:
            result[property.name] = {'name': property.name, 'description': property.description}
    for choice in choices:
        if choice.description:
            i = 1
            name = choice.value
            if result.has_key(name):
                name = choice.value + str(i)
                while result.has_key(name):
                    i += 1
                    name = choice.value + str(i)
            result[name] = {'name': choice.value, 'property': choice.property.name, 'description': choice.description}
    
    keys = result.keys()
    keys.sort()
    context['return_resul'] = []
    for key in keys:
        context['return_resul'].append(result[key])
    return render_to_response('catalog/glossarium.html', context)

#def action(request):
#    context = get_default_context(request)
#    action = Product.objects.filter(is_exist=True, is_enabled=True).order_by('id')
#    context['result'] = []
#    for a in action:
#        if a.position_pricing_if_exists() and a.size_is_exists():
#            result.append(a)
#    return render_to_resonse('catalog/action.html', context)

def action_list(request, page=None):
    context = get_default_context(request)
    context['actions'] = Action.objects.filter(is_active=True)
    paginate(
        context, 'actions', 
        Action.objects.filter(is_active=True).order_by('-id'),
        count=COLLECTIONS_ON_PAGE, page=page, 
        root=context['current_section'].path
    )
    context['disables'] = Action.objects.filter(is_active=False).order_by('-id')
    return render_to_response('action/action.html', context)

def action_item(request, slug, page=None):
    context = get_default_context(request)
    context['action'] = get_object_or_404(Action, slug=slug)
    context['crumbs'].append({
      'caption': context['action'].name,
      'path': slug,
    })
    paginate(
        context, 'positions', 
        query=Action.objects.get(slug=slug).products.all().filter(is_enabled=True),
        count=PRODUCTS_ON_PAGE, page=page, 
        root=context['current_section'].path+slug+'/'
    )
    return render_to_response('action/action-item.html', context)

@staff_required
def action_index(request, id):
    context = get_default_context(request)
    nodes = Section.objects.filter(is_enabled=True).values()
    context['structure'] = build_tree(nodes)
    context['action_id'] = id
    return render_to_response('change_action/index.html', context)

@staff_required
def action_catalog(request, id):
    context = get_default_context(request)
    product_in_actions = Action.objects.get(pk=id)
    action_id = []
    for product in product_in_actions.products.all():
        action_id.append(product.id)
    context['action_id'] = action_id
    context['catalog'] = Product.objects.filter(section=Section.get_node_by_path(request.POST['current_section'])).order_by('-order')
    return render_to_response('change_action/catalog.html', context)

@staff_required
def action_add(request, id, add_id):
    context = get_default_context(request)
    action = Action.objects.get(pk=id)
    product = Product.objects.get(pk=add_id)
    action.products.add(product)
    return HttpResponse('Product #%s add in %s action' % (add_id, id))

@staff_required
def action_del(request, id, del_id):
    context = get_default_context(request)
    action = Action.objects.get(pk=id)
    product = Product.objects.get(pk=del_id)
    action.products.remove(product)
    return HttpResponse('Product #%s delete %s action' % (del_id, id))

def nova(request):
    context = get_default_context(request)
    products = Product.objects.filter(is_exist=True).order_by('-date', '-order')
    context['positions'] = []
    for product in products:
        if product.nova():
            context['positions'].append(product)
    return render_to_response('catalog/nova.html', context)
