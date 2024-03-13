from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
from django_htmx.middleware import HtmxDetails
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.cache import cache_page
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

##############################################
# Create your views here.
@login_required
def main_view(request):

    random_category = random.choice(Category.objects.all())
    random_picture = random.choice(CoreImages.objects.all())

    context = {
        'image' : random_picture,
        'category' : random_category,
        'bottles': Bottle.objects.filter(sorting="1"),
    }
    return render(request,'Academy/home.html', context)



##############################################
#CATEGORIES

#Main view
@login_required
@cache_page(60*30)
def category_view(request: HtmxHttpRequest, tag=None) -> HttpResponse:

    random_picture = random.choice(CoreImages.objects.all())

    #add related blogposts


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
        obj = get_object_or_404(Category, subcategory=category)
        related_blogs = Blog.objects.filter(category_tag__subcategory=category).order_by('-blog_date_create')[:2]
        bottle = Bottle.objects.filter(category__subcategory=category)
    except:
        obj = get_object_or_404(Category, name=category)
        related_blogs = Blog.objects.filter(category_tag__name=category).order_by('-blog_date_create')[:2]
        bottle = Bottle.objects.filter(category__name=category)
     
    context = {
        'category': obj,
        'bottles' : bottle,
        'related_blogs' : related_blogs
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


##############################################
#BOTTLES
@login_required
def bottles_list_view(request, brand=None):
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

    return render(request,'Academy/bottles_list.html', context)

@login_required
def bottle_detail_view(request, item=None):
    obj = Bottle.objects.get(slug=item)
    country = obj.brand.country_of_origin

    context = {
        'bottle' : obj,
        'country' : country,
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
def dashboard_list_view(request, item):
    name_to_model_class = {
    'Category' : Category,
    'Bottle': Bottle,
    'Brand' : Brand,
    'Blog' : Blog,
    }
    
    obj_item = name_to_model_class[item]
    obj = obj_item.objects.all()

    context = {
        'objects': obj,
        'type': item
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
        'Blog': Blog,
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


@login_required
def dashboard_edit_item(request, type=None, item=None):
    name_to_model_class = {
        'Category' : Category,
        'Bottle': Bottle,
        'Brand' : Brand,
        'Blog' : Blog,
        }
    
    name_to_form_class = {
        'Category' : CategoryForm,
        'Bottle': BottleForm,
        'Brand' : BrandForm,
        'Blog' : BlogForm,
    }

    object_model = name_to_model_class[type]
    object = get_object_or_404(object_model, id=item)
    form = name_to_form_class[type](request.POST  or None, request.FILES  or None, instance=object)


    context = {
        'form':form,
        'object':object
    }

    if form.is_valid():
        form.save()
        context['message'] = 'Data saved'

    return render(request,'Academy/dashboard_crud.html',context)

@login_required
def dashboard_create_item(request, type=None):
   
    name_to_form_class = {
        'Category' : CategoryForm,
        'Bottle': BottleForm,
        'Brand' : BrandForm,
        'Blog' : BlogForm,
    }

    if request.method == 'POST':
        form = name_to_form_class[type](request.POST, request.FILES)
        if form.is_valid():
            object = form.save()
            return redirect(object.get_absolute_url())
    else:
        form = name_to_form_class[type]
    
    context = {
        'form' : form
    }

    return render(request, 'Academy/dashboard_crud.html', context)
    


##############################################
# AGE GATE  


def age_gate_view(request):

    #Load the original page after checking age gate.
    next_url = request.session['next_url']

    #Register users IP for age gate.
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    try:
        ip =ip
    except:
        ip = 'none'

    form = AgeGateForm({'ip':ip})
    
    #Store age gate response
    if request.method == 'POST':
        form = AgeGateForm(request.POST or None,  {'ip':ip})
        if form.is_valid():
            form.save()
            request.session['agegate'] = 'welcome'
            return redirect(next_url)
    
    context = {
        'form':form,
    }

    return render(request,'Academy/agegate.html', context)

##############################################
# BLOG


@login_required
def blog_detail_view(request, slug=None):

    blog = get_object_or_404(Blog, slug=slug)
    context = {
        'blog' : blog
    }

    return render(request,'Academy/blog.html', context)    

@login_required
def blog_list_view(request):
        
    blogs = Blog.objects.all()
    
    context = {
        'blogs' : blogs
    }

    return render(request,'Academy/blog_list.html', context)

@login_required
def blog_image_uploader(request):
    pass





###################################################
#test

def test_view(request):

    obj = Blog.objects.all()

    obj2 = Blog.objects.filter(Q(category_tag__subcategory='Cognac') | Q(brand_tag__name='') | Q(bottle_tag__name='Dry Gin'))


    context = {
        'obj' : obj,
        'obj2':obj2,
    }

    return render(request,'Academy/test.html',context)

def placeholder_view(request):
    return render(request,'Academy/placeholder.html')