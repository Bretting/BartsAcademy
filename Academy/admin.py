from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

class BrandAdmin(admin.ModelAdmin):
    search_fields = ['name']


class BottleResource(resources.ModelResource):
    class Meta:
            model = Bottle

class BottleAdmin(ImportExportModelAdmin):
    search_fields = ['name', 'category__name', 'category__subcategory']
    resource_classes = [BottleResource]

class BlogAdmin(admin.ModelAdmin):
    search_fields = ['name', 'category_tag__name', 'category_tag__subcategory']
    list_display = ['name', 'blog_date_create', 'blog_date_edit']

class RecipeAdmin(admin.ModelAdmin):
     search_fields = ['name']

class RecipeIngredientAdmin(admin.ModelAdmin):
     search_fields = ['related_recipe', 'related_product', 'unrelated_product']
     list_display = ['related_recipe', 'related_product', 'unrelated_product', 'amount', 'type']



admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Bottle, BottleAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(CoreImages)
admin.site.register(AgeGate)
admin.site.register(BlogImage)
admin.site.register(BlogType)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)