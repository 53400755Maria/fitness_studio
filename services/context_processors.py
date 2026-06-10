from .models import Category, Tag

def get_sidebar_data(request):
    return {
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }