from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
from django_htmx.middleware import HtmxDetails
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.forms import inlineformset_factory, modelformset_factory
import pandas as pd
import logging
from .models import (
    CoreImages,
    Category,
    Bottle,
    Brand,
    Blog,
    BlogImage,
)

from .forms import (
    CategoryForm,
    BottleForm,
    BrandForm,
    AgeGateForm,
    BlogForm,
    BlogImageForm,
)
##############################################


#helper class
class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails

##############################################
# Create your views here.
@login_required
def main_view(request):

    random_category = Category.objects.order_by('?').first()
    random_picture = CoreImages.objects.order_by('?').first()

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
def category_view(request: HtmxHttpRequest, tag=None) -> HttpResponse:

    random_picture = CoreImages.objects.order_by('?').first()

    #add related blogposts

    categories = cache.get('category')
    if not categories:
        categories = Category.objects.all()
        cache.set('category', categories, 600)

    context = {
        'categories' : categories,
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

    categories = cache.get('category')
    if not categories:
        categories = Category.objects.all()
        cache.set('category', categories, 600)


    context = {
        'categories' : categories
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
    country_list = Brand.objects.values_list('country_of_origin', flat=True).distinct()

    category_list = Category.objects.exclude(brand__isnull=True)

    brand_list = cache.get('brands')
    if not brand_list:
        brand_list = Brand.objects.all().order_by('sorting')
        cache.set('brands', brand_list, 600)
    

    context = {
        'brands' : brand_list, 
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

        # bottle_list = cache.get('bottles')
        # if not bottle_list:
        bottle_list = Bottle.objects.all()
            # cache.set('bottles', bottle_list, 600)

        context = {
            'bottles' : bottle_list,
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
    related_blogs = Blog.objects.filter(bottle_tag=obj)

    context = {
        'bottle' : obj,
        'country' : country,
        'related_blogs' : related_blogs
    }
    print(related_blogs)

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
        'form' : form,
        'type' : type,
    }

    return render(request, 'Academy/dashboard_crud.html', context)

@login_required
def dashboard_analytics_view(request):

    context = {

    }

    return render(request,'Academy/partials/dashboard-analytics.html', context)
    


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
            if next_url:
                return redirect(next_url)
            else: 
                return redirect("/")
    
    context = {
        'form':form,
    }

    return render(request,'Academy/agegate.html', context)

##############################################
# BLOG


@login_required
def blog_detail_view(request, slug=None):

    blog = get_object_or_404(Blog, slug=slug)
    gallery = BlogImage.objects.filter(related_blog=blog)
    context = {
        'blog' : blog,
        'gallery' : gallery
    }

    return render(request,'Academy/blog.html', context)    

@login_required
def blog_list_view(request: HtmxHttpRequest) -> HttpResponse:
        
    blogs = Blog.objects.all()
    brands = Brand.objects.all()
    categories = Category.objects.all()
    
    context = {
        'blogs' : blogs,
        'brands' : brands,
        'categories' : categories
    }
    if request.htmx:
        return render(request,'Academy/partials/blogs.html', context)

    return render(request,'Academy/blog_list.html', context)


def blog_create_view(request):
    # Create an instance of the BlogForm
    blog_form = BlogForm(request.POST and request.FILES or None)
    BlogImageFormSet = inlineformset_factory(Blog, BlogImage, form=BlogImageForm, extra=2)

    if request.method == 'POST':
        blog_form = BlogForm(request.POST, request.FILES)
        formset = BlogImageFormSet(request.POST, request.FILES)

        if blog_form.is_valid() and formset.is_valid():

            # Save the BlogForm instance
            blog_instance = blog_form.save()

            for form in formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()            

            # Save the formset instances
            instances = formset.save(commit=False)
            for instance in instances:
                instance.related_blog = blog_instance
                instance.save()

            return redirect(blog_instance.get_absolute_url())

    else:
        blog_form = BlogForm()
        formset = BlogImageFormSet()

    context = {
    'blog_form':blog_form,
    'formset':formset
    }

    # Render the template with both forms
    return render(request, 'Academy/blog_crud.html', context)

@login_required
def blog_edit_view(request, item=None):
    
    object = get_object_or_404(Blog, id=item)
    blog_form = BlogForm(request.POST  or None, request.FILES  or None, instance=object)
    BlogImageFormSet = inlineformset_factory(Blog, BlogImage, form=BlogImageForm, extra=0, can_delete=True)
    formset = BlogImageFormSet(request.POST  or None, request.FILES  or None, instance=object)


    if request.method == 'POST':
        # Populate the forms with incoming data
        blog_form = BlogForm(request.POST, request.FILES, instance=object)
        formset = BlogImageFormSet(request.POST, request.FILES, instance=object)

        if blog_form.is_valid() and formset.is_valid():

            # Save the BlogForm instance
            blog_instance = blog_form.save()

            for form in formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()


            # Save the formset instances
            instances = formset.save(commit=False)
            for instance in instances:
                instance.related_blog = blog_instance
                instance.save()

            return redirect(blog_instance.get_absolute_url())
        else:
            print(blog_form.errors)
            print(formset.errors)


    context = {
        'blog_form':blog_form,
        'formset':formset
    }

    return render(request,'Academy/blog_crud.html',context)

@login_required
def blog_filtered_view(request, filter=None):

    if Blog.objects.filter(category_tag__subcategory=filter):
        obj = Blog.objects.filter(category_tag__subcategory=filter)
        print('subcategory')
    elif Blog.objects.filter(category_tag__name=filter):
        obj = Blog.objects.filter(category_tag__name=filter)
        print('Main category')
    else:
        obj = None

    context = {
        'blogs' : obj,
    }


    return render(request,'Academy/partials/blogs.html', context)









###################################################
#test
@login_required
def test_view(request):
    # Create an instance of the BlogForm
    blog_form = BlogForm(request.POST and request.FILES or None)
    BlogImageFormSet = inlineformset_factory(Blog, BlogImage, form=BlogImageForm, extra=2)

    if request.method == 'POST':
        print('posted')
        blog_form = BlogForm(request.POST, request.FILES)
        formset = BlogImageFormSet(request.POST, request.FILES)

        if blog_form.is_valid() and formset.is_valid():
            print('valided')
            # Save the BlogForm instance
            blog_instance = blog_form.save()

            for form in formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()            

            # Save the formset instances
            instances = formset.save(commit=False)
            for instance in instances:
                instance.related_blog = blog_instance
                instance.save()

            return redirect(blog_instance.get_absolute_url())

    else:
        blog_form = BlogForm()
        formset = BlogImageFormSet()

    context = {
        'blog_form':blog_form,
        'formset':formset
    }


    return render(request, 'Academy/test.html', context)










def placeholder_view(request):
    return render(request,'Academy/placeholder.html')


def SKU_importer(request):
    brands = Brand.objects.all()

    if request.method == 'POST' and request.FILES:
        #grab info from the form:
        excel_file = pd.read_excel(request.FILES['file'])
        img_file = request.FILES['img']
        webshop = request.POST['webshop']
        consumer_webshop = request.POST['consumer_webshop']
        website = request.POST['website']
        brand_name= Brand.objects.get(name=request.POST['brand'])
       
        #grab the correct column of info on the template excel file
        data = excel_file.iloc[:,1]
        data = data.fillna("")

        #prepare data for use in Model
        if not data.iloc[17] == None:
            nom = data.iloc[17].capitalize()
        if not data.iloc[18] == None:
            source_material = data.iloc[18].capitalize()
        if not data.iloc[7] == None:
            region = data.iloc[7]
        if not data.iloc[19] == None:
            cooking = data.iloc[19].capitalize()
        if not data.iloc[20] == None:
            extraction = data.iloc[20].capitalize()
        if not data.iloc[21] == None:
            mash = data.iloc[21].title()
        if not data.iloc[22] == None:
            botanicals = data.iloc[22].title()
        if not data.iloc[23] == None:
            water_source = data.iloc[23].capitalize()
        if not data.iloc[24] == None:
            fermentation = data.iloc[24].capitalize()
        if not data.iloc[25] == None:
            distillation = data.iloc[25].capitalize()
        if not data.iloc[26] == None:
            filtration = data.iloc[26].capitalize()
        if not data.iloc[27] == None:
            still = data.iloc[27].capitalize()
        if not data.iloc[28] == None:
            batch_size = data.iloc[28]
        if not data.iloc[29] == None:
            blend = data.iloc[29].capitalize()
        if not data.iloc[30] == None:
            aging = data.iloc[30].capitalize()
        if not data.iloc[31] == None:
            aging_barrels = data.iloc[31].capitalize()
        if not data.iloc[32] == None:
            other = data.iloc[32].capitalize()

        #Check if the category exists and if it is a main or a sub category. Print error if it doesn't exist.
        try:
            category_name = Category.objects.get(subcategory=data.iloc[4].capitalize())
        except Category.DoesNotExist:
            try:
                category_name = Category.objects.get(name=data.iloc[4].capitalize())
            except Category.DoesNotExist:
                return HttpResponse(f"Category not found with subcategory or name: {data.iloc[4].capitalize()}")
        except Exception as e:
            return HttpResponse('There is something wrong with the template: ' + e )
        
        bottle_size


        #Check if the object already exists, if not: create.
        try:
            object = Bottle.objects.get(name=data.iloc[3].capitalize(),category=category_name, brand=brand_name)
            if object:
                return HttpResponse('Bottle already exists!')
        except:
            try:
                object = Bottle.objects.create(
                    name = data.iloc[3].capitalize(),
                    category = category_name,
                    sorting = 2,
                    brand = brand_name,
                    bottle_size = data.iloc[8],
                    info = '<p>' + data.iloc[12] + '</p>',
                    tasting_notes = '<p>' +data.iloc[13] + '</p>',
                    abv = data.iloc[6],
                    image = img_file,
                    shop_link=webshop,
                    consumer_shop_link = consumer_webshop,
                    website_link = website,
                    tech_nom = nom,
                    tech_source_material = source_material,
                    tech_region = region,
                    tech_cooking = cooking,
                    tech_extraction = extraction,
                    tech_mash = mash,
                    tech_botanicals = botanicals,
                    tech_water_source = water_source,
                    tech_fermentation = fermentation,
                    tech_distillation = distillation,
                    tech_filtration = filtration,
                    tech_still = still,
                    tech_batch_size = batch_size,
                    tech_blend = blend,
                    tech_aging = aging,
                    tech_aging_barrels = aging_barrels,
                    tech_other = other
                )

                object.save()
                return redirect(object.get_absolute_url())
            except:
                return HtmxHttpRequest('Something went wrong. Please doublecheck the excel-template')
        
    context = {
        'brands' : brands
    }

    return render(request,'Academy/sku_importer.html', context)