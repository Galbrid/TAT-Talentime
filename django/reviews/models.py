from django.conf import settings
from django.db import models


class UserReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=150, blank=True)
    rating = models.PositiveSmallIntegerField(default=0)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Review'
        verbose_name_plural = 'User Reviews'

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.rating})"
        if self.user:
            return f"{self.user.username} ({self.rating})"
        return f"Anonymous ({self.rating})"
