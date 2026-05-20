# core/urls.py

from django.urls import path
from . import views
from .views import CustomLoginView

app_name = 'core'

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
]