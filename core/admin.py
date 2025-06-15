from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.core.cache import cache
from django import forms
from .models import *

admin.site.site_header = "Learn it Admin"
admin.site.site_title = "Learn it Admin Portal"
admin.site.index_title = "Welcome to Learn it Admin Dashboard"

# Custom User Appearence in admin panel
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'country' in self.data:  # If a country is selected in the form
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by("name")
            except (ValueError, TypeError):
                pass  # Handle invalid country_id
        elif self.instance.pk and self.instance.country:  # If editing an existing user
            self.fields['city'].queryset = City.objects.filter(country=self.instance.country).order_by("name")
        else:
            self.fields['city'].queryset = City.objects.none()  # Empty city dropdown by default


class CustomUserAdmin(UserAdmin):

    form = CustomUserForm

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "headline", "email", "phone1", "phone2", "country", "city", "profile_picture")}),
        ("Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    list_display = ("username", "email", "role", "is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email")
    ordering = ("username",)

    # Optional: Make password readonly in the admin panel to prevent unwanted errors
    readonly_fields = ("password",)

    def save_model(self, request, obj, form, change):
        if change:
            original = User.objects.get(pk=obj.pk)
            if original.role != obj.role:
                cache.delete(f"user_token_{obj.pk}")  # Invalidate token
        
        super().save_model(request, obj, form, change)

admin.site.register(User, CustomUserAdmin)

# Register models to admin site

admin.site.register(StudentProfile)
admin.site.register(InstructorProfile)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(CourseSyllabus)
admin.site.register(CourseLearningOutcome)
admin.site.register(CourseSection)
admin.site.register(CourseLesson)
admin.site.register(Track)
# admin.site.register(TrackGroup)
# admin.site.register(CourseGroup) # Business Dashboard
admin.site.register(TrackEnrollment)
# admin.site.register(Enrollment) # Business Dashboard - Course Enrollment
# admin.site.register(Payment) # Business Dashboard
# admin.site.register(Installment) # Business Dashboard
# admin.site.register(CourseReview) # Business Dashboard
# admin.site.register(TrackCertificate) # Business Dashboard
admin.site.register(CourseRequirement) 
# admin.site.register(Quiz) # Business Dashboard
# admin.site.register(QuizQuestion) # Business Dashboard
# admin.site.register(QuizAnswer) # Business Dashboard
# admin.site.register(QuizAttempt) # Business Dashboard
admin.site.register(Event)
admin.site.register(EventImage)
admin.site.register(CourseFAQ)
admin.site.register(TrackFAQ)
# admin.site.register(Country) # Business Dashboard
# admin.site.register(Nationality) # Business Dashboard
# admin.site.register(City) # Business Dashboard
admin.site.unregister(Group)