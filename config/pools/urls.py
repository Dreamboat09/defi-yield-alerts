from django.urls import path
from . import views

urlpatterns = [
    path('', views.pool_list, name='pool_list'),
    path('sync/', views.sync_pools, name='sync_pools'),
    path('<str:pool_id>/', views.pool_detail, name='pool_detail'),
]