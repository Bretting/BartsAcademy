from django.urls import path
from .views import (
    main_view,
    category_view,
    category_select_view,
    category_global_view,
    category_filtered_view,
    brand_view,
    brand_filtered_view,
    brand_overview,
    bottle_view,
    bottle_detail_view,
    bottle_filtered_view,
    bottle_create_view,
    bottle_update_view
)

app_name = 'Academy'
urlpatterns = [
    path('', main_view, name='home'),

    ######################
    #CATEGORIES
    path('Categories',category_view, name='categories'),
    path('Categories/<str:category>',category_select_view,name='category_filter'),
    path('Category-global', category_global_view,name='category-global'),
    path('Category-global/<str:object>',category_filtered_view,name='category-global-filtered'),
    ######################
    #BRANDS
    path('Brands',brand_view,name='brands'),
    path('Brands-filtered/<str:filter>',brand_filtered_view,name='brand-filtered'),
    path('Brand/<str:brandname>',brand_overview,name='brand-overview'),

    ######################
    #BOTTLES
    path('Bottles/<str:brand>',bottle_view,name='bottles'),
    path('Bottle/<str:item>', bottle_detail_view, name='bottle_detail'),
    path('Bottles-filtered/<str:filter>',bottle_filtered_view,name='bottle_filtered'),
    path('Bottle-create',bottle_create_view,name='bottle-crud'),
    path('Bottle-update/<int:id>',bottle_update_view,name='bottle-update'),


   ######################
    #TEST VIEW
]
