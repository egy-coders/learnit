from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta, datetime



# Country
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, null=True, blank=True)  # ISO Alpha-2 or Alpha-3
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name
        
# Nationality
class Nationality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Nationalities"

    def __str__(self):
        return self.name

# City
class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        unique_together = ('name', 'country')  # Ensures no duplicate city names in the same country
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.name}, {self.country.name}"

# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    headline = models.CharField(max_length=100, blank=True, null=True)
    phone1 = models.CharField(max_length=15, blank=True, null=True)
    phone2 = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, related_name="users", blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, related_name="users", blank=True, null=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, related_name="users", blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Change this
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Change this
        blank=True
    )

    # USERNAME_FIELD = 'username'  # Login with username instead of username

    class Meta:
        db_table = 'custom_user'

    def __str__(self):
        return self.username

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    rate = models.PositiveSmallIntegerField(default=1) # later for recruitment in need talents section
    code = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        verbose_name_plural = "Students"

    def __str__(self):
        return f'@{self.user.username} | {self.user.first_name} {self.user.last_name}'

class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'instructor'})
    bio = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='student_resumes/', null=True, blank=True)
    social_links = models.JSONField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name_plural = "Instructors"

    def __str__(self):
        return f'@{self.user.username} | {self.user.first_name} {self.user.last_name} - Rating: {self.rating}'


# Track Model
class Track(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="track_images/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True) # Website Price / Each Course Group has its own prices
    discount = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],  # Ensures 0% - 100%
        help_text="Enter discount percentage (0 to 100)",
        default=0,
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Course Category Model
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

# Resize image before upload
from PIL import Image
from io import BytesIO
from django.core.files import File

# Course Model
class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    CURRENCY_CHOICES = [
        ('EGP', 'EGP'),
        ('USD', 'USD'),
        ('SAR', 'SAR'),
        ('AED', 'AED'),
    ]
    title = models.CharField(max_length=255)
    excerpt = models.TextField(blank=True, null=True)
    description = models.TextField()
    platform = models.CharField(max_length=50, blank=True, null=True) # zoom, skype, meetings ...
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=20, choices=CURRENCY_CHOICES, default='EGP')
    discount = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],  # Ensures 0% - 100%
        help_text="Enter discount percentage (0 to 100)",
        default=0
    )
    tracks = models.ManyToManyField(Track,  blank=True, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(User, related_name='courses', limit_choices_to={'role':'student'}, blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    countdown_date = models.DateField(null=True, blank=True) # in advertising on landingpage
    featured = models.BooleanField(default=0) # Badge on course card
    best_seller = models.BooleanField(default=0) # Badge on course card
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Handle thumbnail image before save
    def save(self, *args, **kwargs):
        if self.thumbnail:
            img = Image.open(self.thumbnail)

            # Force resize (will stretch if needed)
            img = img.resize((410, 378), Image.Resampling.LANCZOS)

            # Convert RGBA to RGB to support JPEG
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Save resized image to BytesIO
            thumb_io = BytesIO()
            img_format = img.format or 'JPEG'  # Default to JPEG if format is None
            img.save(thumb_io, format=img_format)

            # Replace the file in the model
            self.thumbnail.save(self.thumbnail.name, File(thumb_io), save=False)

        super().save(*args, **kwargs)



    @property
    def average_rating(self):
        avg_rating = self.reviews.aggregate(avg_score=Avg('score'))['avg_score']
        return round(avg_rating, 1) if avg_rating else 0  # Round to 1 decimal place

    def discounted_price(self):
        """Calculate the price after discount."""
        return self.price * (1 - self.discount / 100)

    def __str__(self):
        return f"{self.title}"

# Track FAQ Model
class TrackFAQ(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    position = models.PositiveSmallIntegerField(default=1) # Frontend order


# Learning Outcomes Model
# what you will learn by the end of this course
class CourseLearningOutcome(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='outcomes')
    outcome = models.TextField()
    position = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = "Course Outcomes"

    def __str__(self):
        return f"{self.course.title} - {self.outcome}"


# Course Syllabus Model
class CourseSyllabus(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='syllabuses')
    title = models.CharField(max_length=255)
    description = models.TextField()
    position = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = "Courses Syllabuses"

    def __str__(self):
        return f"{self.course.title} - {self.title}"


# Course Sections Model
class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    position = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

# Course Lessons Model
class CourseLesson(models.Model):
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_url = models.URLField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    position = models.PositiveIntegerField(default=1)

    
    def __str__(self):
        return f"{self.section.title} - {self.title}"

# Course Requirement / Prerequisite Model
class CourseRequirement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="requirements")
    requirement = models.CharField(max_length=255)
    position = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.requirement} | {self.course.title}"

# Course FAQ Model
class CourseFAQ(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    position = models.PositiveSmallIntegerField(default=1) # Frontend order

# # Group for each track (multiple courses) -- start new track round
# class TrackGroup(models.Model):
#     track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="groups")
#     instructors = models.ManyToManyField(User, limit_choices_to={'role': 'instructor'})
#     start_date = models.DateField()
#     end_date = models.DateField()

#     def __str__(self):
#         return f"{self.track.title} - {self.start_date}"

# Group for each single course -- start new course round
class CourseGroup(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="groups")
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'instructor'}, related_name='instructors', null=True, blank=True)
    students = models.ManyToManyField(User, related_name='students', limit_choices_to={'role': 'student'})
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.course.title} - {self.start_date} - {self.instructor.first_name} {self.instructor.last_name}"

# Full Track Enrollments Model
class TrackEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    # group = models.ForeignKey(TrackGroup, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'track')

    def __str__(self):
        return f"{self.user.username} - {self.track.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for course in self.track.courses.all():
            # Pick any available group (or skip if none)
            course_group = CourseGroup.objects.filter(course=course).first()
            if course_group:
                Enrollment.objects.get_or_create(user=self.user, course=course, group=course_group)



# Enrollments Model (Course)
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text='Percentage completion', null=True, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  # Prevent duplicate enrollment
    
    def __str__(self):
        return f"{self.course.title} - {self.user.first_name} {self.user.last_name}"

# Payments Model
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('Paymob', 'Paymob'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    PAYMENT_TYPE_CHOICES = [
        ('cash', 'Cash'),
        ('installment', 'Installment')
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student', limit_choices_to={'role':'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin', limit_choices_to={'role':'admin'})
    # For Installments
    total_installments = models.PositiveIntegerField(default=1)
    paid_installments = models.PositiveIntegerField(default=0)
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    
    def __str__(self):
        return f"{self.course.title} - {self.user.first_name} {self.user.last_name} - {self.payment_type} - {self.amount}"

    # Check if installments are completed or not
    def is_completed(self):
        return self.paid_installments == self.total_installments

    def create_installments(self):
        # Create installments based on the total installments and the installment amount
        for i in range(self.total_installments):
            due_date = self.created_at.date() + timedelta(days=30*(i+3))  # Installment due date set every 3 months
            Installment.objects.create(
                payment=self,
                installment_number=i+1,
                amount=self.installment_amount,
                due_date=due_date
            )

    

# CourseGroup Installment 
class Installment(models.Model):
    INSTALLMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='installments')
    installment_number = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=INSTALLMENT_STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"User: {self.payment.user.first_name} {self.payment.user.last_name} - Installment {self.installment_number} for {self.payment.course.title} - Amount: {self.amount}"

    def is_overdue(self):
        return self.due_date < datetime.today().date() and self.status != 'paid'


# Course Reviews Model
class CourseReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.course.title} - {self.user.first_name} {self.user.last_name} - {self.rating}"


# Track Certificates Model
class TrackCertificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'student'})
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_url = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.track.title} - {self.user.first_name} {self.user.last_name} - {self.issued_at}"

# Course Certificates Model
class CourseCertificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'course')  # Only one certificate per course per user

    def __str__(self):
        return f"{self.course.title} - {self.user.get_full_name()} - {self.issued_at}"


# Quiz Model
class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Quizzes"

# Quiz Question Model
class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()

# Quiz Answer Model
class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="answers")
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

# Quiz Attempt Model
class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'quiz')  # Only one attempt allowed per user

# Event Model
class Event(models.Model):
    TYPE_CHOICES = [
        ('webinar', 'Webinar'),
        ('conference', 'Conference'),
        ('seminar', 'Seminar'),
        ('workshop', 'Workshop'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    location = models.CharField(max_length=250, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='events_photos/', blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.title}"

class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='photo_gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='api/events_images/')
    position = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Image for {self.event.title}"

class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    info = models.TextField()
    order = models.PositiveIntegerField(default=1)

class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=255)
    info = models.TextField()
    order = models.PositiveIntegerField(default=1)

class TermsConditions(models.Model):
    title = models.CharField(max_length=255)
    info = models.TextField()
    order = models.PositiveIntegerField(default=1)

class TalentRequest(models.Model):
    user_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)  # Use your existing Country model
    company_name = models.CharField(max_length=150)
    position = models.CharField(max_length=100)
    job_description = models.TextField()
    salary_range = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.position}"

class Contact(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=150)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.company_name}"