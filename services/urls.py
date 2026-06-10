from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='home'),
    path('category/<slug:cat_slug>/', views.service_list, name='category'),
    path('tag/<slug:tag_slug>/', views.service_list, name='tag'),
    path('service/<slug:service_slug>/', views.service_detail, name='service_detail'),
    path('add/', views.AddService.as_view(), name='add_service'),
    path('about/', views.about, name='about'),
]