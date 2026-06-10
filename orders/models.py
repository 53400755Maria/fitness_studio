from django.db import models
from django.conf import settings
from services.models import Service

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтверждён'),
        ('completed', 'Выполнен'),
        ('canceled', 'Отменён'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name='Клиент')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')
    booking_date = models.DateField(verbose_name='Дата бронирования')
    booking_time = models.TimeField(verbose_name='Время бронирования')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        return f'Заказ #{self.id} от {self.user.username} на {self.service.title}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'