from django.urls import path

from .views import LoginView, MeView, RegisterView, RoleListView

urlpatterns = [
    path('api/auth/register', RegisterView.as_view(), name='register'),
    path('api/auth/login', LoginView.as_view(), name='login'),
    path('api/auth/me', MeView.as_view(), name='me'),
    path('api/admin/roles', RoleListView.as_view(), name='roles'),
]
