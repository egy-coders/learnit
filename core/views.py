from django.shortcuts import render, get_object_or_404
from .models import *



def home(request):
    context = {
        'page_title' : 'Home Page',
    }
    return render(request, 'core/home.html', context)

# All Tracks
def tracks(request):
    tracks = Track.objects.all()
    context = {
        'page_title' : 'Our Tracks',
        'tracks' : tracks,
    }
    return render(request, 'core/tracks.html', context)

# Single Track
def track(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    context = {
        'page_title' : track.title,
        'track' : track,
    }
    return render(request, 'core/track.html', context)

# All Courses
def courses(request):
    courses = Course.objects.all()
    context = {
        'page_title' : 'Our Courses',
        'courses' : courses,
    }
    return render(request, 'core/courses.html', context)

# Single Course
def course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    context = {
        'page_title' : course.title,
        'course' : course,
    }
    return render(request, 'core/course.html', context)


def about(request):
    context = {
        'page_title' : 'About Us'
    }
    return render(request, 'core/about.html', context)
    
def faqs(request):
    context = {
        'page_title' : 'FAQs'
    }
    return render(request, 'core/faqs.html', context)

def contact(request):
    context = {
        'page_title' : 'Contact'
    }
    return render(request, 'core/contact.html', context)