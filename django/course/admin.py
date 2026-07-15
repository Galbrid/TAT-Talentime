from django.contrib import admin
from .models import Category, Status, Course, Enrolled


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_code', 'category', 'level', 'price', 'status', 'created_at')
    list_filter = ('category', 'level', 'status', 'created_at')
    search_fields = ('name', 'course_code', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)


@admin.register(Enrolled)
class EnrolledAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'enrolled_date')
    list_filter = ('status', 'enrolled_date', 'course__category')
    search_fields = ('student__email', 'student__first_name', 'student__last_name', 'course__name')
    readonly_fields = ('enrolled_date', 'updated_at')
    ordering = ('-enrolled_date',)
