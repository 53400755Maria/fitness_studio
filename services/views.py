from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Category, Tag, Service
from .forms import ServiceForm

def service_list(request, cat_slug=None, tag_slug=None):
    services = Service.objects.filter(is_published=True)
    title = 'Услуги фитнес-студии'
    if cat_slug:
        category = get_object_or_404(Category, slug=cat_slug)
        services = services.filter(category=category)
        title = f'Категория: {category.name}'
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        services = services.filter(tags=tag)
        title = f'Тэг: {tag.name}'
    return render(request, 'services/service_list.html', {'services': services, 'title': title})

def service_detail(request, service_slug):
    service = get_object_or_404(Service, slug=service_slug, is_published=True)
    return render(request, 'services/service_detail.html', {'service': service})

class AddService(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = ServiceForm
    template_name = 'services/add_service.html'
    success_url = reverse_lazy('services:home')
    permission_required = 'services.add_service'
def about(request):
    return render(request, 'services/about.html', {'title': 'О фитнес-клубе'})