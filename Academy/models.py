from django.db import models
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField
from django_resized import ResizedImageField

import pathlib


#Custom functions
def image_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    if instance.subcategory:
        new_fname = f"{instance.subcategory}"
    else:
        new_fname = f"{instance.name}"
    return f"{instance.img_location}/{new_fname}{fpath.suffix}"

def video_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_fname = f"{instance.name}"
    return f"{instance.img_location}/{new_fname}{fpath.suffix}"





# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique = True)
    subcategory = models.CharField(max_length=255, unique = True)
    slug = models.SlugField(unique=True)
    info = HTMLField()
    image = ResizedImageField(size=[1000,1000], upload_to=image_upload_handler)
    video = models.FileField(upload_to=video_upload_handler, blank=True, null=True)
    image_location = 'categories'

    def save(self, *args, **kwargs):
        if self.subcategory:
            self.slug = slugify(self.subcategory)
        else:
            self.slug = slugify(self.name)




class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ManyToManyField(Category)
    owner = models.CharField(max_length=255)
    story = HTMLField()
    country_of_origin = models.CharField(max_length=255)
    image = ResizedImageField(size=[1000,1000], upload_to=image_upload_handler)
    image_location = 'brands'
    video = models.FileField(upload_to=video_upload_handler, blank=True, null=True)




class Bottle(models.Model):
    class displaySorting(models.IntegerChoices):
        Lighthouse = 1
        Regular = 2

    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sorting = models.IntegerField(choices = displaySorting.choices,verbose_name='Regular or Lighthouse product')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    info = HTMLField()
    tasting_notes = HTMLField()
    abv = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Alcohol %')
    image = ResizedImageField(size=[1000,1000], upload_to=image_upload_handler)
    shop_link = models.URLField()
    consumer_shop_link = models.URLField()




class Blog(models.Model):
    name = models.CharField(max_length=255)
    blog_teaser = HTMLField()
    blog_image = ResizedImageField(size=[1000,600],upload_to=image_upload_handler, null=True, blank=True)
    blog_text = HTMLField()
    blog_video = models.FileField(upload_to='videos', null=True, blank=True)
    blog_footer_image = ResizedImageField(size=[1000,600],upload_to=image_upload_handler)
    blog_date_create = models.DateField(auto_now_add=True, null=True, blank=True)
    blog_date_edit = models.DateField(auto_now=True, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    img_location = 'blog'
