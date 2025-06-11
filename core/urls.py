from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('faqs/', faqs, name='faqs'),
    path('contact/', contact, name='contact'),
    path('tracks/', tracks, name='tracks'),
    path('tracks/<int:track_id>/', track, name='track'),
    path('courses/', courses, name='courses'),
    path('courses/<int:course_id>/', course, name='course'),
]