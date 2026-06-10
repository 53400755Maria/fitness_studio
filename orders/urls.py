from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/<slug:service_slug>/', views.create_order, name='create_order'),
    path('success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('all/', views.all_orders, name='all_orders'),
    path('change-status/<int:order_id>/', views.change_status, name='change_status'),
    path('report/', views.report, name='report'),
]