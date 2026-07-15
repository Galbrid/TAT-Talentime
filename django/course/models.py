from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Course category."""
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Status(models.Model):
    """Enrollment status choices."""
    CHOICES = [
        ('pending', 'Pending'),
        ('denied', 'Denied'),
        ('active', 'Active'),
    ]

    name = models.CharField(max_length=20, choices=CHOICES, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Statuses"

    def __str__(self):
        return self.get_name_display()


class Course(models.Model):
    """Course model moved from portal app."""
    STATUS_CHOICES = [('draft', 'Draft'), ('published', 'Published'), ('hidden', 'Hidden')]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    course_code = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)
    level = models.CharField(max_length=50, default='Beginner')
    duration = models.CharField(max_length=100, blank=True)
    eligibility = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    instructor = models.CharField(max_length=255, blank=True)
    syllabus = models.TextField(blank=True)
    curriculum = models.TextField(blank=True)
    highlights = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    batch_timings = models.CharField(max_length=255, blank=True)
    placement_details = models.TextField(blank=True)
    certification = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


def get_default_status():
    """Get default status (Pending)."""
    status, _ = Status.objects.get_or_create(name='pending')
    return status.pk


class Enrolled(models.Model):
    """Student course enrollment tracking."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='course_enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, default=get_default_status)
    enrolled_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student} - {self.course} ({self.status})'
