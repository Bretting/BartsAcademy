from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
from django_htmx.middleware import HtmxDetails
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db.models import Q
from django.forms import inlineformset_factory
from django.urls import reverse
import os
import json
import boto3
from django.http import JsonResponse
from django.views import generic
import pandas as pd
from .models import (
    CoreImages,
    Category,
    Bottle,
    Brand,
    Blog,
    BlogImage,
    Recipe,
    RecipeIngredient,
    BlogVideo,
)

from .forms import (
    CategoryForm,
    BottleForm,
    BrandForm,
    AgeGateForm,
    BlogForm,
    BlogImageForm,
    RecipeForm,
    RecipeIngredientForm,
)
##############################################


#helper class
class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails

##############################################
# Create your views here.
def main_view(request):

    random_category = Category.objects.order_by('?').first()
    random_picture = CoreImages.objects.order_by('?').first()
    random_recipes = Recipe.objects.all().order_by('?')[:3]

    context = {
        'image' : random_picture,
        'category' : random_category,
        'bottles': Bottle.objects.filter(sorting="1").prefetch_related('brand'),
        'blog' : Blog.objects.order_by('pk').last(),
        'recipes' : random_recipes
    }
    return render(request,'Academy/home.html', context)



##############################################
#CATEGORIES

#Main view
def category_view(request: HtmxHttpRequest, tag=None) -> HttpResponse:

    random_picture = CoreImages.objects.order_by('?').first()

    #add related blogposts

    categories = cache.get('category')
    if not categories:
        categories = Category.objects.all()
        cache.set('category', categories, 3600)

    context = {
        'categories' : categories,
        'image' : random_picture,
    }
    if request.htmx:
        return render(request,'Academy/partials/categories.html', context)
    else:
        return render(request,'Academy/categories.html', context)


#Category detail view
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
    return render(request,'Academy/category_detailview.html', context)

#Filter by global categories
def category_global_view(request):

    categories = cache.get('category')
    if not categories:
        categories = Category.objects.all()
        cache.set('category', categories, 3600)


    context = {
        'categories' : categories
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
    country_list = Brand.objects.values_list('country_of_origin', flat=True).distinct()

    category_list = Category.objects.exclude(brand__isnull=True)

    brand_list = cache.get('brands')
    if not brand_list:
        brand_list = Brand.objects.all().order_by('sorting')
        cache.set('brands', brand_list, 3600)
    

    context = {
        'brands' : brand_list, 
        'country_list' : country_list,
        'category_list' : category_list,
    }

    if request.htmx:
        return render(request,'Academy/partials/brands.html', context)
    else:
        return render(request,'Academy/brands-list.html',context)

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

#Detailview of a brand
def brand_detailview(request, brandname):
    brand = get_object_or_404(Brand.objects.prefetch_related('category'), name=brandname)
    bottles = Bottle.objects.filter(brand__name=brandname)
    related_blogs = Blog.objects.filter(brand_tag=brand)
    

    context = {
        'brand': brand,
        'bottles':bottles,
        'related_blogs' : related_blogs,
    }

    return render(request,'Academy/brand_detailview.html',context)


##############################################
#BOTTLES
def bottles_list_view(request, brand=None):
    country_list = Brand.objects.values_list('country_of_origin', flat=True).distinct()
    category_list = Category.objects.exclude(brand__isnull=True)

    context = {
            'country_list' : country_list,
            'category_list' : category_list,
        }

    if brand=='All':

        bottle_list = cache.get('bottles')
        if not bottle_list:
            bottle_list = Bottle.objects.all().prefetch_related('brand')
            cache.set('bottles', bottle_list, 3600)

        context.update({
            'bottles' : bottle_list,
        })
    else:
        context.update({
            'bottles' : Bottle.objects.filter(brand__name=brand),
        })

    return render(request,'Academy/bottles_list.html', context)

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

    return render(request,'Academy/bottle_detailview.html', context)

def bottle_filtered_view(request, filter=None):

    if Bottle.objects.filter(category__subcategory=filter):
        obj = Bottle.objects.filter(category__subcategory=filter)
    elif Bottle.objects.filter(category__name=filter):
        obj = Bottle.objects.filter(category__name=filter)
    elif Bottle.objects.filter(brand__country_of_origin=filter):
        obj = Bottle.objects.filter(brand__country_of_origin=filter)
    else:
        obj = Bottle.objects.all()

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
    'Recipe' : Recipe
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
        'Recipe' : Recipe
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
        'Recipe' : Recipe
        }
    
    name_to_form_class = {
        'Category' : CategoryForm,
        'Bottle': BottleForm,
        'Brand' : BrandForm,
        'Blog' : BlogForm,
        'Recipe' : RecipeForm,
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
        'Recipe' : RecipeForm
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
        "ingredient_form" : RecipeIngredientForm            
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

    try:
        next_url = request.session['next_url']
    except:
        next_url = '/'

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



def blog_detail_view(request, slug=None):

    blog = get_object_or_404(Blog.objects.prefetch_related('brand_tag', 'category_tag'), slug=slug)
    gallery = BlogImage.objects.filter(related_blog=blog)
    related_brand = blog.brand_tag.all()
    related_bottles = blog.bottle_tag.all()

    bottles = Bottle.objects.filter(Q(brand__in=related_brand) | Q(id__in=related_bottles)).select_related('brand').distinct().order_by('?')

    context = {
        'blog' : blog,
        'gallery' : gallery,
        'related_bottles' : bottles
    }

    return render(request,'Academy/blog_detailview.html', context)    

def blog_list_view(request: HtmxHttpRequest) -> HttpResponse:
    # Use prefetch_related to fetch related Category objects
    blogs = Blog.objects.all().select_related('type_tag').prefetch_related('category_tag', 'brand_tag', 'bottle_tag')

    # Create a dictionary for categories dropdown in the template
    categories = {}

    # Loop through each blog entry
    for blog in blogs:
        # Fetch categories associated with the blog
        categories_list = blog.category_tag.all()

        # Add categories to the dictionary
        for category in categories_list:
            if category.subcategory:
                if category.subcategory not in categories:
                    categories[category.subcategory] = category
            else:
                if category.name not in categories:
                    categories[category.name] = category
    
    context = {
        'blogs': blogs,
        'categories': categories
    }
    if request.htmx:
        return render(request, 'Academy/partials/blogs.html', context)

    return render(request, 'Academy/blog_list.html', context)

@login_required
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


def blog_filtered_view(request: HtmxHttpRequest, type=None, filter=None) -> HttpResponse:

    if type == 'category':
        if Blog.objects.filter(category_tag__subcategory=filter):
            obj = Blog.objects.filter(category_tag__subcategory=filter)
        elif Blog.objects.filter(category_tag__name=filter):
            obj = Blog.objects.filter(category_tag__name=filter)
        else:
            obj = None
    elif type == 'type':
        if Blog.objects.filter(type_tag__name=filter):
            obj = Blog.objects.filter(type_tag__name=filter)
        else:
            obj = None
    else:
        obj = None

    brands = Brand.objects.all()
    blogs = Blog.objects.all()

    #create dictionary for categories dropdown in template.
    categories = {}

    #Loop through each blog entry
    for blog in blogs:
        #Fetch categories associated with the blog
        categories_list = blog.category_tag.all()

        #Add categories to the dictionary
        for category in categories_list:
            if category.subcategory:
                if category.subcategory not in categories:
                    categories[category.subcategory] = category
            else:
                if category.name not in categories:
                    categories[category.name] = category

    context = {
        'blogs' : obj,
        'brands' : brands,
        'categories' : categories
    }

    if request.htmx:
        return render(request,'Academy/partials/blogs.html', context)
    else:
        return render(request,'Academy/blog_list.html', context)


###################################################
#RECIPES


def recipe_view(request:HtmxHttpRequest) -> HttpResponse:

    recipes = Recipe.objects.all()
    type = Recipe.typeSorting.choices
    taste = Recipe.tasteSorting.choices
    occasion = Recipe.occasionSorting.choices

    context = {
        'recipes' : recipes,
        'type_options' : type,
        'taste_options' : taste,
        'occasion_options' : occasion,
    }

    if request.htmx:
        return render(request,'Academy/partials/recipe_list.html', context)
    else:
        return render(request, 'Academy/recipe_list.html', context)

def recipe_detailview(request, slug=None):

    recipe = get_object_or_404(Recipe, slug=slug)
    ingredients = RecipeIngredient.objects.filter(related_recipe=recipe)
    bottles = Bottle.objects.filter(id__in=ingredients.values_list('related_product_id', flat=True))

    context = {
        'recipe' : recipe,
        'ingredients' : ingredients,
        'bottles' : bottles
    }

    return render (request, 'Academy/recipe_detailview.html', context)


def recipe_filtered_view(request: HtmxHttpRequest, sort=None, filter=None) -> HttpResponse:

    type_lookup = {label: value for value, label in Recipe.typeSorting.choices}
    occasion_lookup = {label: value for value, label in Recipe.occasionSorting.choices}
    taste_lookup = {label: value for value, label in Recipe.tasteSorting.choices}

    # Filter the recipes based on the type and corresponding option number
    if sort == 'taste':
        option_number = taste_lookup.get(filter)
        if option_number is not None:
            recipes = Recipe.objects.filter(taste=option_number)
    elif sort == 'occasion':
        option_number = occasion_lookup.get(filter)
        if option_number is not None:
            recipes = Recipe.objects.filter(occasion=option_number)
    elif sort == 'type':
        option_number = type_lookup.get(filter)
        if option_number is not None:
            recipes = Recipe.objects.filter(type=option_number)


    type = Recipe.typeSorting.choices 
    taste = Recipe.tasteSorting.choices
    occasion = Recipe.occasionSorting.choices

    context = {
        'recipes' : recipes,
        'type_options' : type,
        'taste_options' : taste,
        'occasion_options' : occasion,
    }

    if request.htmx:
        return render(request,'Academy/partials/recipe_list.html', context)
    else:
        return render(request, 'Academy/recipe_list.html', context)

@login_required
def recipe_create_view(request):
    # Create an instance of the BlogForm
    recipe_form = RecipeForm(request.POST and request.FILES or None)
    IngredientFormSet = inlineformset_factory(Recipe, RecipeIngredient, form=RecipeIngredientForm, extra=2)

    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        formset = IngredientFormSet(request.POST, request.FILES)

        if recipe_form.is_valid() and formset.is_valid():

            # Save the BlogForm instance
            recipe_instance = recipe_form.save()

            for form in formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()            

            # Save the formset instances
            instances = formset.save(commit=False)
            for instance in instances:
                instance.related_recipe = recipe_instance
                instance.save()

            return redirect(recipe_instance.get_absolute_url())

    else:
        recipe_form = RecipeForm()
        formset = IngredientFormSet()

    context = {
    'recipe_form':recipe_form,
    'formset':formset
    }

    # Render the template with both forms
    return render(request, 'Academy/recipe_crud.html', context)

@login_required
def recipe_edit_view(request, item=None):
    
    object = get_object_or_404(Recipe, id=item)
    recipe_form = RecipeForm(request.POST  or None, request.FILES  or None, instance=object)
    IngredientFormSet = inlineformset_factory(Recipe, RecipeIngredient, form=RecipeIngredientForm, extra=0, can_delete=True)
    formset = IngredientFormSet(request.POST  or None, request.FILES  or None, instance=object)


    if request.method == 'POST':
        # Populate the forms with incoming data
        recipe_form = RecipeForm(request.POST, request.FILES, instance=object)
        formset = IngredientFormSet(request.POST, request.FILES, instance=object)

        if recipe_form.is_valid() and formset.is_valid():

            # Save the BlogForm instance
            recipe_instance = recipe_form.save()

            for form in formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()


            # Save the formset instances
            instances = formset.save(commit=False)
            for instance in instances:
                instance.related_recipe = recipe_instance
                instance.save()

            return redirect(recipe_instance.get_absolute_url())
        else:
            print(recipe_form.errors)
            print(formset.errors)


    context = {
    'recipe_form':recipe_form,
    'formset':formset
    }

    # Render the template with both forms
    return render(request, 'Academy/recipe_crud.html', context)


###################################################
#test
@login_required
def test_view(request):

    recipes = Recipe.objects.all()
    type = Recipe.typeSorting.choices
    taste = Recipe.tasteSorting.choices
    occasion = Recipe.occasionSorting.choices

    context = {
        'recipes' : recipes,
        'type_options' : type,
        'taste_options' : taste,
        'occasion_options' : occasion,
    }
 
    return render(request, 'Academy/test.html', context)


@login_required
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
        
        bottle_text = data.iloc[8]
        if not str(bottle_text).isnumeric():
            bottle_text_filter = filter(str.isdigit, bottle_text)
            bottle_size = "".join(bottle_text_filter)
        else:
            bottle_size = bottle_text



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
                    bottle_size = bottle_size,
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
                return HttpResponse('Something went wrong. Please doublecheck the excel-template')
        
    context = {
        'brands' : brands
    }

    return render(request,'Academy/sku_importer.html', context)


# View to render the upload form with the list of blogs
class UploadView(LoginRequiredMixin,generic.CreateView):
    template_name = "Academy/upload.html"
    model = BlogVideo
    fields = ['file']
 
    def get_success_url(self):
        return reverse("Academy:upload")
 
    def get_context_data(self, **kwargs):
        context = super(UploadView, self).get_context_data(**kwargs)
        context.update({
            "uploads": BlogVideo.objects.all()
        })
        return context

class SignedURLView(LoginRequiredMixin ,generic.View):
    def post(self, request, *args, **kwargs):
        session = boto3.session.Session()
        client = session.client(
            "s3",
            region_name='ams3',
            endpoint_url=os.environ.get('AWS_ENDPOINT_URL'),
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )
 
        url = client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": "media",
                "Key": f"chunks/{json.loads(request.body)['fileName']}",
            },
            ExpiresIn=3000,
        )
        return JsonResponse({"url": url})
    


import os
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from .models import BlogVideo

class MergeChunksView(View):
    def post(self, request):
        file_name = request.POST.get('fileName')
        related_blog_id = request.POST.get('related_blog_id')
        
        # Assuming chunks are saved in the MEDIA_ROOT directory
        chunk_folder = os.path.join(settings.MEDIA_ROOT, 'chunks', file_name)
        final_file_path = os.path.join(settings.MEDIA_ROOT, 'videos', file_name)

        with open(final_file_path, 'wb') as final_file:
            # Sort chunks to ensure they are merged in the correct order
            for chunk_file in sorted(os.listdir(chunk_folder)):
                chunk_file_path = os.path.join(chunk_folder, chunk_file)
                with open(chunk_file_path, 'rb') as chunk:
                    final_file.write(chunk.read())
        
        # Clean up chunks
        for chunk_file in os.listdir(chunk_folder):
            os.remove(os.path.join(chunk_folder, chunk_file))
        os.rmdir(chunk_folder)
        
        # Save final video URL to the model
        final_file_url = os.path.join('videos', file_name)
        BlogVideo.objects.create(
            related_blog_id=related_blog_id,
            file=final_file_url
        )

        return JsonResponse({'success': True, 'url': final_file_url})


from django.http import JsonResponse
import json
from django.conf import settings

@login_required
def uploadVideoView(request):
    if request.method == 'POST':
        try:
            # Extract and parse the JSON data from the request body
            data = json.loads(request.body)
            print('Received data:', data)

            file_name = data.get('fileName')
            total_chunks = data.get('totalChunks')
            signed_urls = data.get('signedUrls')  # Get the list of presigned URLs
            
            # Define the folder to store chunks
            chunk_folder = os.path.join(settings.MEDIA_ROOT, 'chunks')
            if not os.path.exists(chunk_folder):
                os.makedirs(chunk_folder)
            
            # Path to the final merged file
            final_file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)

            # Merge chunks into the final file
            with open(final_file_path, 'wb') as final_file:
                for i in range(total_chunks):
                    chunk_file_path = os.path.join(chunk_folder, f'{file_name}.part{i}')
                    if os.path.exists(chunk_file_path):
                        with open(chunk_file_path, 'rb') as chunk_file:
                            final_file.write(chunk_file.read())
                    else:
                        return JsonResponse({'message': f'Chunk {i} not found.'}, status=404)
            
            # Optionally, delete chunk files after merging
            for i in range(total_chunks):
                chunk_file_path = os.path.join(chunk_folder, f'{file_name}.part{i}')
                if os.path.exists(chunk_file_path):
                    os.remove(chunk_file_path)
            
            # Response indicating success
            return JsonResponse({'message': 'Video uploaded and merged successfully!', 'location': final_file_path})

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            print(f'Error: {e}')
            return JsonResponse({'message': str(e)}, status=500)

    # If GET request, render the upload page
    context = {
        'blogs': Blog.objects.all()
    }

    return render(request, 'Academy/uploadVideo.html', context)

