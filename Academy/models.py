from django.db import models
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField
from django_resized import ResizedImageField
from django.urls import reverse
from django.core.validators import MaxValueValidator

import pathlib


#Custom functions
def image_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)

    try:
        if instance.subcategory == None:
            new_fname = f"{instance.name}"
            return f"{instance.image_location}/{new_fname}{fpath.suffix}"
        else:
            new_fname = instance.subcategory   
            return f"{instance.image_location}/{new_fname}{fpath.suffix}"
    except:
        new_fname = f"{instance.name}"
        return f"{instance.image_location}/{new_fname}{fpath.suffix}"

def logo_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)

    try:
        if instance.subcategory == None:
            new_fname = f"{instance.name}-logo"   
            return f"{instance.image_location}/{new_fname}{fpath.suffix}"
        else:
            new_fname = f"{instance.subcategory}-logo"   
            return f"{instance.image_location}/{new_fname}{fpath.suffix}"
    except:
        new_fname = f"{instance.name}-logo"
        return f"{instance.image_location}/{new_fname}{fpath.suffix}"



def video_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_fname = f"{instance.name}"
    return f"{instance.image_location}/{new_fname}{fpath.suffix}"





# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255, unique = True, blank=True, null=True)
    teaser = HTMLField()
    slug = models.SlugField(unique=True, blank=True)
    info = HTMLField()
    image = ResizedImageField(size=[1000,1000], upload_to=image_upload_handler)
    logo = ResizedImageField(size=[500,500], upload_to=logo_upload_handler)
    video = models.FileField(upload_to='image', blank=True, null=True)
    image_location = 'categories'

    class Meta:
        ordering = ['name','subcategory']

    def save(self, *args, **kwargs):
        if self.subcategory:
            self.slug = slugify(f'{self.name}-{self.subcategory}')
        else:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        if self.subcategory:
            return self.subcategory
        else:
            return self.name
        
    def get_overview_link(self):
        if self.subcategory:
            return reverse('Academy:category_filter', kwargs={'category':self.subcategory})
        else:
            return reverse('Academy:category_filter', kwargs={'category':self.name})            




class Brand(models.Model):
    class displaySorting(models.IntegerChoices):
        Lighthouse = 1
        Regular = 2

    name = models.CharField(max_length=255, unique=True)
    sorting = models.IntegerField(choices = displaySorting.choices,verbose_name='Regular or Lighthouse product')
    category = models.ManyToManyField(Category)
    owner = models.CharField(max_length=255)
    story = HTMLField()
    country_of_origin = models.CharField(max_length=255)
    image = ResizedImageField(size=[1000,1000], upload_to=image_upload_handler)
    image_location = 'brands'
    video = models.FileField(upload_to=video_upload_handler, blank=True, null=True)

 
    def __str__(self):
        return self.name

    def get_bottle_by_brand_link(self):
        return reverse('Academy:brand-overview', kwargs={'brandname':self.name})
    
    def get_brands_by_category_link(self):
        return reverse('Academy:brand-filtered', kwargs={'filter':self.category})
    
    def get_brand_by_country_link(self):
        return reverse('Academy:brand-country', kwargs={'country':self.country_of_origin})



class Bottle(models.Model):
    class displaySorting(models.IntegerChoices):
        Lighthouse = 1
        Regular = 2

    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sorting = models.IntegerField(choices = displaySorting.choices,verbose_name='Sort order')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    bottle_size = models.IntegerField(validators=[MaxValueValidator(9999)])
    info = HTMLField()
    tasting_notes = HTMLField()
    abv = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Alcohol %')
    image = ResizedImageField(size=[1000,1000], upload_to=image_upload_handler)
    shop_link = models.URLField()
    consumer_shop_link = models.URLField()
    website_link = models.URLField()
    tech_nom = models.CharField(max_length=7,blank=True, null=True,verbose_name='NOM')
    tech_source_material = models.CharField(blank=True, null=True, max_length=255, verbose_name='Source material')
    tech_region = models.CharField(blank=True, null=True, max_length=255, verbose_name='Region')
    tech_cooking = models.CharField(blank=True, null=True, max_length=255, verbose_name='Cooking method')
    tech_extraction = models.CharField(blank=True, null=True, max_length=255, verbose_name='Extraction method')
    tech_mash = models.CharField(blank=True, null=True, max_length=255, verbose_name='Mash')
    tech_botanicals = models.CharField(blank=True,null=True, max_length=255, verbose_name='Botanicals')
    tech_water_source = models.CharField(blank=True, null=True, max_length=255, verbose_name='Water source')
    tech_fermentation = HTMLField(blank=True, null=True, verbose_name='Fermentation info')
    tech_distillation = models.CharField(blank=True, null=True, max_length=255, verbose_name='Distillation')
    tech_filtration = models.CharField(blank=True, null=True, max_length=255, verbose_name='Filtration')
    tech_still = models.CharField(blank=True, null=True, max_length=255, verbose_name='Still type')
    tech_batch_size = models.CharField(blank=True, null=True, max_length=255, verbose_name='Batch size')
    tech_blend = models.CharField(blank=True, null=True, max_length=255, verbose_name='Blend')
    tech_aging = models.CharField(blank=True, null=True, max_length=255, verbose_name='Aging')
    tech_aging_barrels = models.CharField(blank=True, null=True, max_length=255, verbose_name='Barrel(s)')
    tech_other = HTMLField(blank=True, null=True, verbose_name='Other')
    slug = models.SlugField(unique=True, blank=True)
    image_location = 'bottles'

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.brand}-{self.name}")
        super(Bottle, self).save(*args, **kwargs)

    def __str__(self):
        return (f"{self.brand} - {self.name}")
    
    class Meta:
        ordering = ['category', 'name']

    def get_bottle_link(self):
        return reverse('Academy:bottle_detail', kwargs={'item':self.slug})




class Blog(models.Model):
    name = models.CharField(max_length=255, unique=True)
    blog_teaser = HTMLField()
    blog_image = ResizedImageField(size=[1000,600],upload_to=image_upload_handler, null=True, blank=True)
    blog_text = HTMLField()
    blog_video = models.FileField(upload_to='videos', null=True, blank=True)
    blog_footer_image = ResizedImageField(size=[1000,600],upload_to=image_upload_handler)
    blog_date_create = models.DateField(auto_now_add=True, null=True, blank=True)
    blog_date_edit = models.DateField(auto_now=True, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image_location = 'blog'

    def __str__(self):
        return self.name


class CoreImages(models.Model):
    image = ResizedImageField(size=[1000,1000],upload_to='core_images')

    def __str__(self):
        return str(self.image)