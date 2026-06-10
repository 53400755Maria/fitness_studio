from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'slug', 'description', 'price', 'duration', 'category', 'tags', 'photo', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }