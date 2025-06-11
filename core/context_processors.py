from .models import Track, Course, Category

def header_context(request):
    return {
        'tracks': Track.objects.all(),
        'courses': Course.objects.all(),
        'cats': Category.objects.all(),
    }
