from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    otp = models.CharField(max_length=6, blank=True)
    otp_expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def has_role(self, role_slug):
        return self.role_mappings.filter(role__slug=role_slug, is_active=True).exists()

    @property
    def role_names(self):
        return [mapping.role.slug for mapping in self.role_mappings.filter(is_active=True)]

    def __str__(self):
        return self.get_full_name() or self.email


class UserRoleMapping(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='role_mappings', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, related_name='user_mappings', on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f'{self.user} -> {self.role}'
