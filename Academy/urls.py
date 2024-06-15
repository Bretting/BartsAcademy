from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import sitemaps
from .views import (
    test_view,
    main_view,
    category_view,
    category_select_view,
    category_global_view,
    category_filtered_view,
    brand_view,
    brand_filtered_view,
    brand_detailview,
    bottles_list_view,
    bottle_detail_view,
    bottle_filtered_view,
    dashboard_view,
    dashboard_list_view,
    dashboard_delete_view,
    dashboard_edit_item,
    dashboard_create_item,
    dashboard_analytics_view,
    age_gate_view,
    blog_detail_view,
    blog_list_view,
    blog_create_view,
    blog_edit_view,
    blog_filtered_view,
    SKU_importer,
)

app_name = 'Academy'
urlpatterns = [
    path('', main_view, name='home'),

    ######################
    #CATEGORIES
    path('Categories',category_view, name='categories'),
    path('Categories/<str:category>',category_select_view,name='category_filter'),
    path('Category-global', category_global_view,name='category_global'),
    path('Category-global/<str:object>',category_filtered_view,name='category_global_filtered'),

    ######################
    #BRANDS
    path('Brands',brand_view,name='brands'),
    path('Brands-filtered/<str:filter>',brand_filtered_view,name='brand_filtered'),
    path('Brand/<str:brandname>',brand_detailview,name='brand_detailview'),

    ######################
    #BOTTLES
    path('Bottles/<str:brand>',bottles_list_view,name='bottles_list'),
    path('Bottle/<str:item>', bottle_detail_view, name='bottle_detail'),
    path('Bottles-filtered/<str:filter>',bottle_filtered_view,name='bottle_filtered'),

    ######################
    #BLOG
    path('Blog/<str:slug>',blog_detail_view, name='blog_detail'),
    path('Blog',blog_list_view, name='blog_list'),
    path('Blog-filtered/<str:filter>',blog_filtered_view,name='blogs_filtered'),

   ######################
    #DASHBOARD
    path('Dashboard',dashboard_view,name='dashboard'),
    path('Dashboard-analytics', dashboard_analytics_view, name='analytics-dashboard'),
    path('Dashboard-list/<str:item>', dashboard_list_view,name='dashboard_list'),
    path('Dashboard-delete/<int:id>-<str:item>',dashboard_delete_view,name='dashboard_delete'),
    path('Dashboard-edit-item/<str:type>-<str:item>', dashboard_edit_item, name='dashboard_edit'),
    path('Dashboard-create-item/<str:type>', dashboard_create_item, name='dashboard_create'),
    path('Dashboard-create-blog', blog_create_view, name='blog_create'),
    path('Dashboard-edit-blog/<str:item>',blog_edit_view, name='blog_edit'),
    path('Dashboard-import',SKU_importer, name='sku_importer'),



   ######################
    #AGEGATE
    path('agegate',age_gate_view,name='agegate'),




    ####################
    #TEST
    path('test',test_view,name='test'),

    ######################
    #Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
