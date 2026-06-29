from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import Course, Enrolled
from course.serializers import CourseSerializer
from .models import Application, Booking, Certificate, Inquiry, Payment, Resource
from .serializers import ApplicationSerializer, BookingSerializer, CertificateSerializer, InquirySerializer, PaymentSerializer, ResourceSerializer

User = get_user_model()


class PublicCourseListView(ListAPIView):
    queryset = Course.objects.filter(status='published').order_by('-created_at')
    serializer_class = CourseSerializer


class CourseDetailView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class InquiryCreateView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = InquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Inquiry received.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingCheckView(APIView):
    permission_classes = []

    def get(self, request):
        booking_id = request.query_params.get('bookingId', '').strip()
        phone = request.query_params.get('phone', '').strip()
        name = request.query_params.get('name', '').strip()

        queryset = Booking.objects.all()
        if booking_id:
            queryset = queryset.filter(booking_id__icontains=booking_id)
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
        if name:
            queryset = queryset.filter(name__icontains=name)

        serializer = BookingSerializer(queryset.order_by('-created_at')[:20], many=True)
        return Response({'success': True, 'count': queryset.count(), 'bookings': serializer.data})


class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrollments = Enrolled.objects.filter(student=request.user).order_by('-enrolled_date')
        certificates = Certificate.objects.filter(user=request.user).order_by('-earned_date')
        payments = Payment.objects.filter(user=request.user).order_by('-payment_date')
        resources = Resource.objects.all().order_by('-created_at')

        data = {
            'enrolledCourses': [
                {
                    'id': enrollment.course.id,
                    'name': enrollment.course.name,
                    'instructor': enrollment.course.instructor or 'TBD',
                    'progress': 0 if enrollment.status.name == 'pending' else 100,
                    'status': enrollment.status.name,
                }
                for enrollment in enrollments
            ],
            'certificates': CertificateSerializer(certificates, many=True).data,
            'payments': PaymentSerializer(payments, many=True).data,
            'resources': ResourceSerializer(resources, many=True).data,
            'totalHours': 0,
        }
        return Response(data)


class StudentApplyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('courseId') or request.data.get('course_id')
        if not course_id:
            return Response({'message': 'courseId is required.'}, status=status.HTTP_400_BAD_REQUEST)

        course = Course.objects.filter(pk=course_id).first()
        if not course:
            return Response({'message': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

        application, created = Application.objects.get_or_create(user=request.user, course=course, defaults={'status': 'pending'})
        
        # Create enrollment mapping
        Enrolled.objects.get_or_create(student=request.user, course=course)

        return Response({'message': 'Application submitted.' if created else 'Application already exists.', 'application': ApplicationSerializer(application).data})


class StudentCourseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrollments = Enrolled.objects.filter(student=request.user).order_by('-enrolled_date')
        payload = []
        for enrollment in enrollments:
            payload.append({
                'id': enrollment.course.id,
                'name': enrollment.course.name,
                'description': enrollment.course.description,
                'category': enrollment.course.category.name if enrollment.course.category else 'General',
                'duration': enrollment.course.duration,
                'progress': 0 if enrollment.status.name == 'pending' else 100,
                'status': enrollment.status.name,
            })
        return Response(payload)


class StudentApplicationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        applications = Application.objects.filter(user=request.user).order_by('-applied_date')
        return Response(ApplicationSerializer(applications, many=True).data)


class StudentCertificateListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        certificates = Certificate.objects.filter(user=request.user).order_by('-earned_date')
        return Response(CertificateSerializer(certificates, many=True).data)


class StudentPaymentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user=request.user).order_by('-payment_date')
        return Response(PaymentSerializer(payments, many=True).data)


class StudentResourceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resources = Resource.objects.all().order_by('-created_at')
        return Response(ResourceSerializer(resources, many=True).data)


class AdminDashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff and not request.user.has_role('admin'):
            return Response({'message': 'Only admins can access this data.'}, status=status.HTTP_403_FORBIDDEN)

        return Response({
            'students': User.objects.filter(role_mappings__role__slug='student').count(),
            'courses': Course.objects.count(),
            'applications': Application.objects.count(),
            'payments': Payment.objects.count(),
            'certificates': Certificate.objects.count(),
        })
