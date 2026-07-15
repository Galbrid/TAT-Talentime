#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tat_backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
u, created = User.objects.get_or_create(
    username='student1',
    defaults={
        'email': 'student@talentime.local',
        'first_name': 'John',
        'last_name': 'Doe'
    }
)
u.set_password('student123')
u.save()
status = 'Created' if created else 'Exists'
print(f"{status}: Student user - {u.get_full_name()}")
