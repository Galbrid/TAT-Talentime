from django.core.management.base import BaseCommand

from accounts.models import Role


class Command(BaseCommand):
    help = 'Seed default roles for the platform'

    def handle(self, *args, **options):
        roles = [
            ('Admin', 'admin', 'Platform administrator'),
            ('Tutor', 'tutor', 'Course instructor'),
            ('Student', 'student', 'Learner'),
        ]

        for name, slug, description in roles:
            Role.objects.get_or_create(slug=slug, defaults={'name': name, 'description': description})

        self.stdout.write(self.style.SUCCESS('Seeded default roles.'))
