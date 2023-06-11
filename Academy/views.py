from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpRequest
from django_htmx.middleware import HtmxDetails
import random
from .models import (
    CoreImages,
    Category,
    Bottle,
    Brand,
)

from .forms import (
    CategoryForm,
    BottleForm
)
##############################################


#helper class
class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails

##############################################
# Create your views here.
def main_view(request):

    random_category = random.choice(Category.objects.all())
    random_picture = random.choice(CoreImages.objects.all())

    context = {
        'image' : random_picture,
        'category' : random_category,
        'bottles': Bottle.objects.all(),
    }
    return render(request,'Academy/home.html', context)


##############################################
#CATEGORIES

#Main view
def category_view(request: HtmxHttpRequest, tag=None) -> HttpResponse:
    random_picture = random.choice(CoreImages.objects.all())
    context = {
        'categories' : Category.objects.all(),
        'image' : random_picture,
    }
    if request.htmx:
        return render(request,'Academy/partials/categories.html', context)
    else:
        return render(request,'Academy/categories.html', context)

#Category detail view
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
def category_global_view(request):
    context = {
        'categories' : Category.objects.all()
    }
    return render(request,'Academy/partials/global-categories.html', context)

#Filter by subcategories
def category_filtered_view(request, object = None):
    obj = Category.objects.filter(name=object)
    context = {
        'categories' : obj
    }

    return render (request,'Academy/partials/categories.html', context)

##############################################
#BRANDS

#Main view
def brand_view(request: HtmxHttpRequest) -> HttpResponse:
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

#Filter Brands
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

def brand_overview(request, brandname):
    brand = Brand.objects.get(name=brandname)
    bottles = Bottle.objects.filter(brand__name=brandname)
    

    context = {
        'brand': brand,
        'bottles':bottles,
    }

    return render(request,'Academy/brands-overview.html',context)


##############################################
#BOTTLES

def bottle_view(request, brand=None):
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

def bottle_detail_view(request, item=None):

    obj = Bottle.objects.get(slug=item)
    country = obj.brand.country_of_origin

    context = {
        'bottle' : obj,
        'country' : country
    }

    return render(request,'Academy/bottle.html', context)

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


def bottle_create_view(request):

    if request.method == 'POST':
        form = BottleForm(request.POST, request.FILES)
        if form.is_valid():
            bottle = form.save()
            return redirect(bottle.get_bottle_link())
    else:
        form = BottleForm
    
    context = {
        'form' : form
    }

    return render(request, 'Academy/bottle_crud.html', context)

def bottle_update_view(request, id=None):
    object = get_object_or_404(Bottle, id=id)
    form = BottleForm(request.POST or None, instance=object)

    context = {
        'form':form,
        'object':object
    }

    if form.is_valid():
        form.save()
        context['message'] = 'Data saved'

    return render(request,'Academy/bottle_crud.html',context)


##############################################
# DASHBOARD

def dashboard_view(request):

    context = {

    }

    return render(request,'Academy/dashboard.html', context)