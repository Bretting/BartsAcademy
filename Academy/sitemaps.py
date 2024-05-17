from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Category, Brand, Bottle, Blog

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['Academy:home', 'Academy:categories', 'Academy:brands', 'Academy:blog_list', 'Academy:agegate']

    def location(self, item):
        return reverse(item)

class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.category_date_edit if obj.category_date_edit else obj.category_date_create

class BrandSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Brand.objects.all()

    def lastmod(self, obj):
        return obj.brand_date_edit if obj.brand_date_edit else obj.brand_date_create

class BottleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return Bottle.objects.all()

    def lastmod(self, obj):
        return obj.bottle_date_edit if obj.bottle_date_edit else obj.bottle_date_create

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.blog_date_edit if obj.blog_date_edit else obj.blog_date_create

sitemaps = {
    'static': StaticViewSitemap,
    'categories': CategorySitemap,
    'brands': BrandSitemap,
    'bottles': BottleSitemap,
    'blogs': BlogSitemap,
}