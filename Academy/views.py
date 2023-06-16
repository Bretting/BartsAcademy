from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpRequest
from django_htmx.middleware import HtmxDetails
from django.contrib.auth.decorators import login_required
import random
from .models import (
    CoreImages,
    Category,
    Bottle,
    Brand,
)

from .forms import (
    CategoryForm,
    BottleForm,
    BrandForm,
)
##############################################


#helper class
class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails

##############################################
# Create your views here.
@login_required
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
@login_required
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

@login_required
def bottle_detail_view(request, item=None):

    obj = Bottle.objects.get(slug=item)
    country = obj.brand.country_of_origin

    context = {
        'bottle' : obj,
        'country' : country
    }

    return render(request,'Academy/bottle.html', context)

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
            return redirect(bottle.get_bottle_link())
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

def placeholder_view(request):
    return render(request,'Academy/placeholder.html')