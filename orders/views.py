from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from .models import Order
from .forms import OrderForm
from services.models import Service

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

@staff_member_required
def all_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders/all_orders.html', {'orders': orders})

@staff_member_required
def change_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
    return redirect('orders:all_orders')

@staff_member_required
def report(request):
    total_orders = Order.objects.count()
    status_stats = Order.objects.values('status').annotate(cnt=Count('id'))
    revenue = Order.objects.filter(status='completed').aggregate(total=Sum('service__price'))['total'] or 0
    popular_services = Order.objects.values('service__title').annotate(cnt=Count('id')).order_by('-cnt')[:5]
    context = {
        'total_orders': total_orders,
        'status_stats': status_stats,
        'revenue': revenue,
        'popular_services': popular_services,
    }
    return render(request, 'orders/report.html', context)