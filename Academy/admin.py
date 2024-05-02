from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

class BrandAdmin(admin.ModelAdmin):
    search_fields = ['name']

class BottleAdmin(admin.ModelAdmin):
    search_fields = ['name', 'category__name', 'category__subcategory']

class BlogAdmin(admin.ModelAdmin):
    search_fields = ['name', 'category_tag__name', 'category_tag__subcategory']
    list_display = ['name', 'blog_date_create', 'blog_date_edit']



admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Bottle, BottleAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(CoreImages)
admin.site.register(AgeGate)
admin.site.register(BlogImage)