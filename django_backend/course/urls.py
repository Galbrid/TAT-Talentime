from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'statuses', views.StatusViewSet)
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'enrollments', views.EnrolledViewSet, basename='enrolled')

urlpatterns = [
    path('', include(router.urls)),
]
