from django.urls import path
from .views import (
    main_view,
    category_view,
    category_select_view,
    category_global_view,
    category_filtered_view,
    category_create_view,
    category_update_view,
    brand_view,
    brand_filtered_view,
    brand_overview,
    brand_update_view,
    brand_create_view,
    bottle_view,
    bottle_detail_view,
    bottle_filtered_view,
    bottle_create_view,
    bottle_update_view,
    dashboard_view,
    dashboard_edit_view,
    dashboard_analytics_view,
    dashboard_delete_view,
    age_gate_view,
    blog_create_view,
    blog_detail_view,
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
    path('Category-create',category_create_view,name='create_Category'),
    path('Category-update/<int:id>',category_update_view,name='category_update'),
    ######################
    #BRANDS
    path('Brands',brand_view,name='brands'),
    path('Brands-filtered/<str:filter>',brand_filtered_view,name='brand_filtered'),
    path('Brand/<str:brandname>',brand_overview,name='brand_overview'),
    path('Brand-create',brand_create_view,name='create_Brand'),
    path('Brand-update/<int:id>',brand_update_view,name='brand_update'),

    ######################
    #BOTTLES
    path('Bottles/<str:brand>',bottle_view,name='bottles'),
    path('Bottle/<str:item>', bottle_detail_view, name='bottle_detail'),
    path('Bottles-filtered/<str:filter>',bottle_filtered_view,name='bottle_filtered'),
    path('Bottle-create',bottle_create_view,name='create_Bottle'),
    path('Bottle-update/<int:id>',bottle_update_view,name='bottle_update'),

    ######################
    #BLOG
    path('Blog-create',blog_create_view, name='create_Blog'),
    path('Blog/<str:slug>',blog_detail_view, name='blog_detail'),

   ######################
    #DASHBOARD
    path('Dashboard',dashboard_view,name='dashboard'),
    path('Dashboard-items/<str:item>', dashboard_edit_view,name='item-dashboard'),
    path('Dashboard-analytics', dashboard_analytics_view, name='analytics-dashboard'),
    path('Dashboard-delete/<int:id>-<str:item>',dashboard_delete_view,name='dashboard_delete'),
   ######################
    #TEST VIEW
    path('agegate',age_gate_view,name='agegate')
]
