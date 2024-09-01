from django.urls import path
from shortener import views
from shortener.views import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index),
    path('register/',views.user_register),
    path('login/', views.user_login),
    path('logout', views.user_logout),
    path('create/', views.create_shortened_url, name='create_shortened_url'),
    path('<str:short_code>/', views. redirect_url, name='redirect_url'),
    path('analytics/', views.url_analytics, name='url_analytics'),



    
    #path('<str:shortcode>/', views.redirect_url, name='redirect_url'),
    # path('shorten/', views.shorten_url, name='shorten_url'),
    # path('<str:shortcode>/', views.redirect_url, name='redirect_url'),
    # path('analytics/<str:shortcode>/', views.view_analytics, name='analytics'),
]
