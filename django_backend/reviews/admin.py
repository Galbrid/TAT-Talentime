from django.contrib import admin
from .models import UserReview


@admin.register(UserReview)
class UserReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'comments')
