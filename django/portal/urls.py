from django.urls import path

from .views import (
    AdminDashboardSummaryView,
    BookingCheckView,
    CourseDetailView,
    InquiryCreateView,
    PublicCourseListView,
    StudentApplicationListView,
    StudentApplyView,
    StudentCertificateListView,
    StudentCourseListView,
    StudentDashboardView,
    StudentPaymentListView,
    StudentResourceListView,
)

urlpatterns = [
    path('api/courses/public', PublicCourseListView.as_view(), name='public-courses'),
    path('api/courses/<int:pk>', CourseDetailView.as_view(), name='course-detail'),
    path('api/inquiries', InquiryCreateView.as_view(), name='inquiries'),
    path('api/bookings/check', BookingCheckView.as_view(), name='booking-check'),
    path('api/student/dashboard', StudentDashboardView.as_view(), name='student-dashboard'),
    path('api/student/apply', StudentApplyView.as_view(), name='student-apply'),
    path('api/student/courses', StudentCourseListView.as_view(), name='student-courses'),
    path('api/student/applications', StudentApplicationListView.as_view(), name='student-applications'),
    path('api/student/certificates', StudentCertificateListView.as_view(), name='student-certificates'),
    path('api/student/payments', StudentPaymentListView.as_view(), name='student-payments'),
    path('api/student/resources', StudentResourceListView.as_view(), name='student-resources'),
    path('api/admin/dashboard', AdminDashboardSummaryView.as_view(), name='admin-dashboard'),
]
