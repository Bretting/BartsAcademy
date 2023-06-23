from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django_htmx.middleware import HtmxDetails
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests
import json
import random
from .models import (
    CoreImages,
    Category,
    Bottle,
    Brand,
    Blog,
)

from .forms import (
    CategoryForm,
    BottleForm,
    BrandForm,
    AgeGateForm,
    BlogForm,
)
##############################################


#helper class
class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails

def get_ip_geolocation_data(ip):
    api_key = settings.GEO_LOCATE_API
    api_url = 'https://ipgeolocation.abstractapi.com/v1/?api_key='+api_key
    response = requests.get(api_url)
    return response.content

##############################################
# Create your views here.
@login_required
def main_view(request):
    if request.session.has_key('agegate'):
        random_category = random.choice(Category.objects.all())
        random_picture = random.choice(CoreImages.objects.all())

        context = {
            'image' : random_picture,
            'category' : random_category,
            'bottles': Bottle.objects.all(),
        }
        return render(request,'Academy/home.html', context)
    else:
        request.session['next_url'] = request.path
        return redirect('/preview/agegate')


##############################################
#CATEGORIES

#Main view
@login_required
def category_view(request: HtmxHttpRequest, tag=None) -> HttpResponse:
    if request.session.has_key('agegate'):
        random_picture = random.choice(CoreImages.objects.all())
        context = {
            'categories' : Category.objects.all(),
            'image' : random_picture,
        }
        if request.htmx:
            return render(request,'Academy/partials/categories.html', context)
        else:
            return render(request,'Academy/categories.html', context)
    else:
        request.session['next_url'] = request.path
        return redirect('/preview/agegate')

#Category detail view
@login_required
def category_select_view(request, category=None):
    try:
        print('sub')
        obj = get_object_or_404(Category, subcategory=category)
    except:
        print('global')
        obj = get_object_or_404(Category, name=category)

    if Bottle.objects.filter(category__subcategory=category):
        bottle = Bottle.objects.filter(category__subcategory=category)
    else: 
        bottle = Bottle.objects.filter(category__name=category)

    context = {
        'category': obj,
        'bottles' : bottle
    }
    return render(request,'Academy/category-overview.html', context)

#Filter by global categories
@login_required
def category_global_view(request):
    context = {
        'categories' : Category.objects.all()
    }
    return render(request,'Academy/partials/global-categories.html', context)

#Filter by subcategories
@login_required
def category_filtered_view(request, object = None):
    obj = Category.objects.filter(name=object)
    context = {
        'categories' : obj
    }

    return render (request,'Academy/partials/categories.html', context)

@login_required
def category_create_view(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            return redirect(category.get_absolute_url())
    else:
        form = CategoryForm
    
    context = {
        'form' : form
    }

    return render(request, 'Academy/dashboard_crud.html', context)

@login_required
def category_update_view(request, id=None):
    object = get_object_or_404(Category, id=id)
    form = CategoryForm(request.POST  or None, request.FILES  or None, instance=object)

    context = {
        'form':form,
        'object':object
    }

    if form.is_valid():
        form.save()
        context['message'] = 'Data saved'

    return render(request,'Academy/dashboard_crud.html',context)

##############################################
#BRANDS

#Main view
@login_required
def brand_view(request: HtmxHttpRequest) -> HttpResponse:
    if request.session.has_key('agegate'):
        random_picture = random.choice(CoreImages.objects.all())
        country_list = Brand.objects.values_list('country_of_origin', flat=True).distinct()

        category_list = Category.objects.exclude(brand__isnull=True)
        

        context = {
            'image' : random_picture,
            'brands' : Brand.objects.all().order_by('sorting'), 
            'country_list' : country_list,
            'category_list' : category_list,
        }

        if request.htmx:
            return render(request,'Academy/partials/brands.html', context)
        else:
            return render(request,'Academy/brands.html',context)
    else:
        request.session['next_url'] = request.path
        return redirect('/preview/agegate')

#Filter Brands
@login_required
def brand_filtered_view(request, filter=None):

    if Brand.objects.filter(category__subcategory=filter):
        obj = Brand.objects.filter(category__subcategory=filter)
    elif Brand.objects.filter(category__name=filter):
        obj = Brand.objects.filter(category__name=filter)
    elif Bottle.objects.filter(brand__name=filter):
        obj = Bottle.objects.filter(brand__name=filter)
    else:
        obj = Brand.objects.filter(country_of_origin=filter)

    context = {
        'brands' : obj,
    }

    return render(request,'Academy/partials/brands.html', context)

@login_required
def brand_overview(request, brandname):
    brand = Brand.objects.get(name=brandname)
    bottles = Bottle.objects.filter(brand__name=brandname)
    

    context = {
        'brand': brand,
        'bottles':bottles,
    }

    return render(request,'Academy/brands-overview.html',context)

@login_required
def brand_create_view(request):

    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            return redirect(category.get_absolute_url())
    else:
        form = BrandForm
    
    context = {
        'form' : form
    }

    return render(request, 'Academy/category_crud.html', context)

@login_required
def brand_update_view(request, id=None):
    object = get_object_or_404(Brand, id=id)
    form = BrandForm(request.POST  or None, request.FILES  or None, instance=object)

    context = {
        'form':form,
        'object':object
    }

    if form.is_valid():
        form.save()
        context['message'] = 'Data saved'

    return render(request,'Academy/dashboard_crud.html',context)


##############################################
#BOTTLES
@login_required
def bottle_view(request, brand=None):
    if request.session.has_key('agegate'):
        country_list = Brand.objects.values_list('country_of_origin', flat=True).distinct()
        category_list = Category.objects.exclude(brand__isnull=True)

        if brand=='All':
            context = {
                'bottles' : Bottle.objects.all(),
                'country_list' : country_list,
                'category_list' : category_list,
            }
        else:
            context = {
                'bottles' : Bottle.objects.filter(brand__name=brand),
                'country_list' : country_list,
                'category_list' : category_list,
            }

        return render(request,'Academy/bottles.html', context)
    else:
        request.session['next_url'] = request.path
        return redirect('/preview/agegate')

@login_required
def bottle_detail_view(request, item=None):
    if request.session.has_key('agegate'):
        obj = Bottle.objects.get(slug=item)
        country = obj.brand.country_of_origin

        context = {
            'bottle' : obj,
            'country' : country
        }

        return render(request,'Academy/bottle.html', context)
    else:
        request.session['next_url'] = request.path
        return redirect('/preview/agegate')

@login_required
def bottle_filtered_view(request, filter=None):

    if Bottle.objects.filter(category__subcategory=filter):
        obj = Bottle.objects.filter(category__subcategory=filter)
    elif Bottle.objects.filter(category__name=filter):
        obj = Bottle.objects.filter(category__name=filter)
    else:
        obj = Bottle.objects.filter(brand__country_of_origin=filter)

    context = {
        'bottles' : obj,
    }

    return render(request,'Academy/partials/bottles.html',context)

@login_required
def bottle_create_view(request):

    if request.method == 'POST':
        form = BottleForm(request.POST, request.FILES)
        if form.is_valid():
            bottle = form.save()
            return redirect(bottle.get_absolute_url())
    else:
        form = BottleForm
    
    context = {
        'form' : form
    }

    return render(request, 'Academy/dashboard_crud.html', context)

@login_required
def bottle_update_view(request, id=None):
    object = get_object_or_404(Bottle, id=id)
    form = BottleForm(request.POST  or None, request.FILES  or None, instance=object)

    context = {
        'form':form,
        'object':object
    }

    if form.is_valid():
        form.save()
        context['message'] = 'Data saved'

    return render(request,'Academy/dashboard_crud.html',context)


##############################################
# DASHBOARD

@login_required
def dashboard_view(request):

    context = {
        'bottles' : Bottle.objects.all(),
        'categories' : Category.objects.all(),
        'brands': Brand.objects.all(),
    }

    return render(request,'Academy/dashboard.html', context)

@login_required
def dashboard_edit_view(request, item):
    name_to_model_class = {
    'Category' : Category,
    'Bottle': Bottle,
    'Brand' : Brand,
    }
    
    obj_item = name_to_model_class[item]
    obj = obj_item.objects.all()
    create_link = f"Academy:create_{item}"

    context = {
        'objects': obj,
        'link' : create_link
    }

    return render(request,'Academy/partials/dashboard-items.html',context)

@login_required
def dashboard_analytics_view(request):

    context = {

    }

    return render(request,'Academy/partials/dashboard-analytics.html', context)


@login_required
def dashboard_delete_view(request, id=None, item=None):

    name_to_model_class = {
        'Bottle': Bottle,
        'Category': Category,
        'Brand':Brand,
    }

    obj_item = name_to_model_class[item]
    obj = obj_item.objects.get(id=id)

    context = {
        'item' : obj
    }

    if request.method == 'POST':
        obj.delete()
        return redirect('Academy:dashboard')
    
    return render(request,'Academy/dashboard-delete.html',context)

##############################################
# AGE GATE  

def age_gate_view(request):

    next_url = request.session['next_url']

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    geolocation_json = get_ip_geolocation_data(ip)
    geolocation_data = json.loads(geolocation_json)
    try:
        country = geolocation_data['country']
        region = geolocation_data['region']
        city = geolocation_data['city']
    except:
        country = 'none'
        region = 'none'
        city = 'none'

    form = AgeGateForm({'country':country,'region':region,'city':city})
    
    if request.method == 'POST':
        form = AgeGateForm(request.POST or None,  {'country':country,'region':region,'city':city})
        if form.is_valid():
            form.save()
            request.session['agegate'] = 'welcome'
            return redirect(next_url)
    
    context = {
        'form':form,
        'test':next_url
    }

    return render(request,'Academy/agegate.html', context)

##############################################
# BLOG

@login_required
def blog_create_view(request):
    form = BlogForm

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save()
            return redirect(blog.get_absolute_url())
    else:
        form = BlogForm
    
    context = {
        'form' : form
    }

    return render(request,'Academy/dashboard_crud.html',context)

@login_required
def blog_detail_view(request, slug=None):

    if request.session.has_key('agegate'):
        blog = get_object_or_404(Blog, slug=slug)
        context = {
            'blog' : blog
        }

        return render(request,'Academy/blog.html', context)

    else:
        request.session['next_url'] = request.path
        return redirect('/preview/agegate')


def placeholder_view(request):
    return render(request,'Academy/placeholder.html')