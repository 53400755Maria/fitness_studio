from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.conf import settings

from .models import Category, Tag, Service
from .forms import ServiceForm
from orders.models import Order
from orders.forms import OrderForm

# ----- ОСНОВНЫЕ ПРЕДСТАВЛЕНИЯ ДЛЯ УСЛУГ -----
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

def map_page(request):
    return render(request, 'services/map_page.html', {'title': 'Наш зал на карте'})

def about_page(request):
    return render(request, 'services/about.html', {'title': 'О фитнес-клубе'})

# ----- ЗАКАЗЫ (если нужно, но они в orders/views, добавлены для полноты) -----
@login_required
def create_order(request, service_slug):
    service = get_object_or_404(Service, slug=service_slug, is_published=True)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.service = service
            order.save()
            return redirect('orders:order_success')
    else:
        form = OrderForm()
    return render(request, 'orders/create_order.html', {'form': form, 'service': service})

@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})

# ----- YANDEXGPT ЧАТ -----
@csrf_exempt
def yandex_gpt_chat(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')

        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Authorization": f"Api-Key {settings.YANDEX_GPT_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "modelUri": f"gpt://{settings.YANDEX_GPT_FOLDER_ID}/yandexgpt-lite/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.5,
                "maxTokens": 2000
            },
            "messages": [
                {
                    "role": "system",
                    "text": "Ты — полезный ассистент фитнес-студии. Отвечай вежливо и только по темам, связанным с фитнесом, услугами студии, здоровым образом жизни. Не отвечай на другие темы."
                },
                {
                    "role": "user",
                    "text": user_message
                }
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        ai_message = result['result']['alternatives'][0]['message']['text']
        return JsonResponse({'response': ai_message})
    except Exception as e:
        print("Ошибка в yandex_gpt_chat:", str(e))
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)