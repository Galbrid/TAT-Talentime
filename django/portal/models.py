from django.conf import settings
from django.db import models
from course.models import Course


class Application(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('enrolled', 'Enrolled')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='applications', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='applications', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} -> {self.course}'


class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='certificates', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='certificates', on_delete=models.CASCADE)
    certificate_number = models.CharField(max_length=100, unique=True)
    earned_date = models.DateTimeField(auto_now_add=True)
    download_url = models.URLField(blank=True)
    qr_code_data = models.TextField(blank=True)

    def __str__(self):
        return self.certificate_number


class Payment(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('completed', 'Completed')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='payments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    invoice_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.amount}'


class Resource(models.Model):
    course = models.ForeignKey(Course, related_name='resources', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='resources/', blank=True)
    file_size = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Inquiry(models.Model):
    STATUS_CHOICES = [('new', 'New'), ('responded', 'Responded')]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=255, default='General Inquiry')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    submitted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Lead(models.Model):
    STATUS_CHOICES = [('new', 'New'), ('contacted', 'Contacted'), ('converted', 'Converted'), ('lost', 'Lost')]

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    source = models.CharField(max_length=100, default='Website Inquiry')
    follow_up_notes = models.TextField(blank=True)
    assigned_staff = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    booking_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=50, default='pending')
    event_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.booking_id
