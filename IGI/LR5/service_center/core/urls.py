# core/urls.py

from django.urls import re_path
from . import views
from .views import CustomLoginView

app_name = 'core'

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^about/$', views.about, name='about'),
    re_path(r'^news/$', views.news_list, name='news_list'),
    re_path(r'^news/(?P<pk>\d+)/$', views.news_detail, name='news_detail'),
    re_path(r'^glossary/$', views.glossary, name='glossary'),
    re_path(r'^contacts/$', views.contacts, name='contacts'),
    re_path(r'^privacy/$', views.privacy, name='privacy'),
    re_path(r'^vacancies/$', views.vacancies, name='vacancies'),
    re_path(r'^reviews/$', views.reviews, name='reviews'),
    re_path(r'^promocodes/$', views.promocodes, name='promocodes'),
    re_path(r'^services/$', views.service_list, name='service_list'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^login/$', CustomLoginView.as_view(), name='login'),
    
    # Мастер
    re_path(r'^master/$', views.master_dashboard, name='master_dashboard'),
    re_path(r'^master/order/(?P<order_id>\d+)/edit/$', views.master_edit_order, name='master_edit_order'),
    
    # Отзывы
    re_path(r'^reviews/add/$', views.review_add, name='review_add'),
    re_path(r'^reviews/(?P<pk>\d+)/edit/$', views.review_edit, name='review_edit'),
    re_path(r'^reviews/(?P<pk>\d+)/delete/$', views.review_delete, name='review_delete'),
    
    # Клиент
    re_path(r'^client/$', views.client_dashboard, name='client_dashboard'),
    re_path(r'^client/order/create/$', views.client_create_order, name='client_create_order'),
    re_path(r'^client/order/(?P<order_id>\d+)/add/$', views.client_add_items, name='client_add_items'),
    re_path(r'^client/order/(?P<order_id>\d+)/remove/(?P<item_type>\w+)/(?P<item_id>\d+)/$', views.client_remove_order_item, name='client_remove_order_item'),
    re_path(r'^client/order/(?P<order_id>\d+)/summary/$', views.client_order_summary, name='client_order_summary'),

    # Админ панель
    re_path(r'^dashboard/orders/$', views.admin_orders, name='admin_orders'),
    re_path(r'^dashboard/order/(?P<order_id>\d+)/$', views.admin_order_detail, name='admin_order_detail'),
    re_path(r'^dashboard/order/create/$', views.admin_order_create, name='admin_order_create'),
    
    # Статистика
    re_path(r'^statistics/$', views.statistics_page, name='statistics'),
]

'''
from django.urls import re_path


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('glossary/', views.glossary, name='glossary'),
    path('contacts/', views.contacts, name='contacts'),
    path('privacy/', views.privacy, name='privacy'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('reviews/', views.reviews, name='reviews'),
    path('promocodes/', views.promocodes, name='promocodes'),
    path('services/', views.service_list, name='service_list'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    
    # Мастер
    path('master/', views.master_dashboard, name='master_dashboard'),
    path('master/order/<int:order_id>/edit/', views.master_edit_order, name='master_edit_order'),
    
    # Отзывы
    path('reviews/add/', views.review_add, name='review_add'),
    path('reviews/<int:pk>/edit/', views.review_edit, name='review_edit'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),
    
    # Клиент
    path('client/', views.client_dashboard, name='client_dashboard'),
    path('client/order/create/', views.client_create_order, name='client_create_order'),
    path('client/order/<int:order_id>/add/', views.client_add_items, name='client_add_items'),
    path('client/order/<int:order_id>/remove/<str:item_type>/<int:item_id>/', views.client_remove_order_item, name='client_remove_order_item'),
    path('client/order/<int:order_id>/summary/', views.client_order_summary, name='client_order_summary'),

    path('dashboard/orders/', views.admin_orders, name='admin_orders'),
    path('dashboard/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('dashboard/order/create/', views.admin_order_create, name='admin_order_create'),
    
    path('statistics/', views.statistics_page, name='statistics'),


]
'''