from django.contrib import admin
from .models import Category, Tag, Service

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'duration', 'category', 'is_published')
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)